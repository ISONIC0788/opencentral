#!/usr/bin/env python3
import base64
import hashlib
import json
import secrets
import socketio
import requests
from collections import defaultdict
from datetime import datetime, UTC
from typing import Dict, Union
from urllib.parse import urlencode, urlparse
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field
from groq import Groq
from db import DB
from cache import REDIS, REDIS_URL
from logger import logger
from utils import stringify
from os import getenv
from dotenv import load_dotenv


load_dotenv()
ALLOWED_SOCKET_ORIGINS = [getenv("SERVER_DOMAIN")] if getenv("SERVER_DOMAIN") else ["http://localhost:8000", "http://localhost:5173", "http://127.0.0.1:8000", "http://127.0.0.1:5173"]
AUTH_SESSION_TTL_SECONDS = 60 * 60 * 24 * 30
AUTH_PENDING_TTL_SECONDS = int(getenv("AUTH_PENDING_TTL_SECONDS") or "900")
DEVICE_CODE_TTL_SECONDS = 60 * 10
DEFAULT_FRONTEND_URL = getenv("FRONTEND_URL") or getenv("SERVER_DOMAIN") or "http://localhost:5173"
AUTH_COOKIE_NAME = getenv("AUTH_COOKIE_NAME") or "logmachine_auth_session"
ROOM_VIEWERS: dict[str, set[str]] = defaultdict(set)
SID_TO_USER: dict[str, str] = {}
SID_TO_ROOMS: dict[str, set[str]] = defaultdict(set)
INFO, DEBUG, WARNING, ERROR = logger.info, logger.debug, logger.warning, logger.error
MAX_QUEUE_SIZE = 100_000


class Message(BaseModel):
    role: str
    content: str

class Data(BaseModel):
    message: str
    history: Union[list[Message], None] = []

class LogEntry(BaseModel):
    user: str
    module: str
    level: str
    timestamp: str = Field(max_length=64)
    message: str


class APIKeyCreateRequest(BaseModel):
    label: str | None = None


class DevicePollRequest(BaseModel):
    device_code: str


class RoomVisibilityRequest(BaseModel):
    visibility: str


class RoomShareRequest(BaseModel):
    username: str
    can_write: bool = False


class OrgCreateRequest(BaseModel):
    name: str = Field(pattern=r"^[ a-zA-Z0-9_-]{3,32}$")


class OrgMemberRequest(BaseModel):
    username: str
    role: str = "developer"


class OrgMemberRoleRequest(BaseModel):
    role: str


class OrgRoomCreateRequest(BaseModel):
    room: str = Field(pattern=r"^[a-zA-Z0-9_-]{3,32}$")
    visibility: str = "private"


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_SOCKET_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=ALLOWED_SOCKET_ORIGINS,
    cors_credentials=True,
    path="/api/socket.io",
    client_manager=socketio.AsyncRedisManager(REDIS_URL, channel="lm:channel:logs")
)
sio_app = socketio.ASGIApp(
    socketio_server=sio,
    other_asgi_app=app,
    socketio_path="/api/socket.io",
)

GroqClient = Groq()
PDB = DB()


def _base_url() -> str:
    return DEFAULT_FRONTEND_URL.rstrip("/")


def _provider_enabled(provider: str) -> bool:
    if provider == "google":
        return bool(getenv("GOOGLE_CLIENT_ID")) and bool(getenv("GOOGLE_CLIENT_SECRET"))
    if provider == "github":
        return bool(getenv("GITHUB_CLIENT_ID") and getenv("GITHUB_CLIENT_SECRET"))
    return False


def _available_providers() -> list[dict[str, str]]:
    providers = []
    if _provider_enabled("google"):
        providers.append({"id": "google", "name": "Google", "description": "Sign in with your Google account"})
    if _provider_enabled("github"):
        providers.append({"id": "github", "name": "GitHub", "description": "Sign in with your GitHub account"})
    return providers


def _random_state() -> str:
    return secrets.token_urlsafe(32)


def _pkce_verifier() -> str:
    return secrets.token_urlsafe(64)


def _pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def _store_pending_auth(provider: str, callback_url: str, redirect_uri: str, verifier: str) -> str:
    state = _random_state()
    payload = {
        "provider": provider,
        "callback_url": callback_url,
        "redirect_uri": redirect_uri,
        "verifier": verifier,
        "created_at": datetime.now(UTC).isoformat(),
    }
    REDIS.setex(f"lm:pending_auth:{state}", AUTH_PENDING_TTL_SECONDS, json.dumps(payload))
    return state


def _get_pending_auth(state: str) -> dict | None:
    if not state:
        return None

    raw = REDIS.get(f"lm:pending_auth:{state}")
    if not raw:
        return None

    try:
        payload = json.loads(raw)
    except Exception:
        REDIS.delete(f"lm:pending_auth:{state}")
        return None

    return payload


def _pop_pending_auth(state: str) -> dict | None:
    if not state:
        return None

    key = f"lm:pending_auth:{state}"
    pipeline = REDIS.pipeline()
    pipeline.get(key)
    pipeline.delete(key)
    raw, _ = pipeline.execute()

    if not raw:
        return None

    try:
        return json.loads(raw)
    except Exception:
        return None


def _attach_device_code_to_pending_auth(state: str, device_code: str) -> bool:
    pending = _get_pending_auth(state)
    if not pending:
        return False

    pending["device_code"] = device_code
    key = f"lm:pending_auth:{state}"
    ttl = REDIS.ttl(key)
    ttl = ttl if ttl and ttl > 0 else AUTH_PENDING_TTL_SECONDS
    REDIS.setex(key, ttl, json.dumps(pending))
    return True


def _callback_target(callback_url: str | None) -> str:
    return callback_url or f"{_base_url()}/auth/callback"


def _build_callback_redirect(callback_url: str, payload: dict[str, str]) -> str:
    separator = "&" if "?" in callback_url else "?"
    return f"{callback_url}{separator}{urlencode(payload)}"


def _is_web_callback(callback_url: str) -> bool:
    try:
        callback = urlparse(callback_url)
        return (
            callback.scheme in {"http", "https"}
            and callback.path.startswith("/auth/callback")
        )
    except Exception:
        return False


def _cookie_secure(request: Request) -> bool:
    env_value = (getenv("AUTH_COOKIE_SECURE") or "yes").strip().lower()
    if env_value in {"1", "true", "yes", "on"}:
        return True
    if env_value in {"0", "false", "no", "off"}:
        return False
    return request.url.scheme == "https"


def _cookie_samesite(secure_cookie: bool) -> str:
    configured = (getenv("AUTH_COOKIE_SAMESITE") or "lax").strip().lower()
    if configured not in {"lax", "strict", "none"}:
        configured = "lax"
    if configured == "none" and not secure_cookie:
        return "lax"
    return configured


def _store_auth_session(user: dict, provider: str, provider_id: str, email: str | None) -> str:
    token = secrets.token_urlsafe(40)
    payload = {
        "token": token,
        "user": stringify(user),
        "provider": provider,
        "provider_id": provider_id,
        "email": email,
        "created_at": datetime.now(UTC).isoformat(),
    }
    REDIS.setex(f"lm:session:{token}", AUTH_SESSION_TTL_SECONDS, json.dumps(payload))
    return token


def _get_auth_session(token: str | None) -> dict | None:
    if not token:
        return None
    raw_session = REDIS.get(f"lm:session:{token}")
    if not raw_session:
        return None

    try:
        session = json.loads(raw_session)
        return session
    except Exception:
        return None


def _delete_auth_session(token: str | None) -> None:
    if not token:
        return
    REDIS.delete(f"lm:session:{token}")


def _resolve_session_user(token: str | None) -> dict | None:
    session = _get_auth_session(token)
    if not session:
        return None
    return session.get("user")


def _resolve_auth_user(credential: str | None) -> dict | None:
    if not credential:
        return None

    session_user = _resolve_session_user(credential)
    if session_user:
        return session_user

    api_user = PDB.resolve_user_by_api_key(credential)
    if api_user:
        return stringify(api_user)

    return None


def _extract_bearer_token(request: Request) -> str | None:
    header = request.headers.get("authorization") or request.headers.get("Authorization")
    if not header or not header.lower().startswith("bearer "):
        return None
    return header.split(" ", 1)[1].strip()


def _extract_auth_token(request: Request) -> str | None:
    return _extract_bearer_token(request) or request.cookies.get(AUTH_COOKIE_NAME)


def _require_auth_user(request: Request) -> dict:
    token = _extract_auth_token(request)
    user = _resolve_auth_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")
    return user


async def _emit_room_presence(room_id: str):
    viewers = list(ROOM_VIEWERS.get(room_id, set()))
    await sio.emit("room:presence", {"room": room_id, "viewers": viewers}, room=room_id)


def _store_device_authorization(device_code: str, auth_token: str, user: dict, provider: str):
    key = f"lm:device:{device_code}"
    raw = REDIS.get(key)
    if not raw:
        return
    try:
        payload = json.loads(raw)
    except Exception:
        return

    payload["status"] = "approved"
    payload["token"] = auth_token
    payload["user"] = stringify(user)
    payload["provider"] = provider
    ttl = REDIS.ttl(key)
    ttl = ttl if ttl and ttl > 0 else DEVICE_CODE_TTL_SECONDS
    REDIS.setex(key, ttl, json.dumps(payload))


@app.get("/api/auth/providers")
def auth_providers():
    return {"providers": _available_providers()}


@app.get("/api/auth/start/{provider}")
def auth_start(
    provider: str,
    request: Request,
    callback_url: str | None = None,
    device_code: str | None = None,
    user_code: str | None = None,
):
    if not _provider_enabled(provider):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested provider is not configured")

    if user_code and not device_code:
        device_code = REDIS.get(f"lm:device_user:{user_code.upper()}")

    if device_code and not REDIS.exists(f"lm:device:{device_code}"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired device code")

    callback_target = _callback_target(callback_url)
    redirect_uri = str(request.url_for("auth_callback", provider=provider))
    verifier = _pkce_verifier()
    challenge = _pkce_challenge(verifier)
    state = _store_pending_auth(provider, callback_target, redirect_uri, verifier)
    if device_code:
        _attach_device_code_to_pending_auth(state, device_code)

    if provider == "google":
        query = {
            "client_id": getenv("GOOGLE_CLIENT_ID"),
            "response_type": "code",
            "scope": "openid email profile",
            "redirect_uri": redirect_uri,
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "prompt": "select_account",
            "access_type": "offline",
        }
        return RedirectResponse(f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(query)}")

    if provider == "github":
        query = {
            "client_id": getenv("GITHUB_CLIENT_ID"),
            "scope": "read:user user:email",
            "redirect_uri": redirect_uri,
            "state": state,
        }
        return RedirectResponse(f"https://github.com/login/oauth/authorize?{urlencode(query)}")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unsupported provider")


@app.get("/api/auth/callback/{provider}", name="auth_callback")
def auth_callback(provider: str, request: Request, code: str | None = None, state: str | None = None, error: str | None = None):
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    if not state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired login session")

    pending = _pop_pending_auth(state)
    if not pending:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired login session")

    if pending.get("provider") != provider:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provider mismatch")

    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization code missing")

    if provider == "google":
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": getenv("GOOGLE_CLIENT_ID"),
                "client_secret": getenv("GOOGLE_CLIENT_SECRET"),
                "code": code,
                "code_verifier": pending["verifier"],
                "grant_type": "authorization_code",
                "redirect_uri": pending["redirect_uri"],
            },
            timeout=10,
        )
        if token_response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google token exchange failed")

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google access token missing")

        profile_response = requests.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        if profile_response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google profile lookup failed")

        profile = profile_response.json()
        provider_id = profile.get("sub")
        display_name = profile.get("name") or profile.get("email") or "Google User"
        email = profile.get("email")
        avatar_url = profile.get("picture")
        username_hint = email.split("@")[0] if email else display_name

    elif provider == "github":
        token_response = requests.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": getenv("GITHUB_CLIENT_ID"),
                "client_secret": getenv("GITHUB_CLIENT_SECRET"),
                "code": code,
                "redirect_uri": pending["redirect_uri"],
                "state": state,
            },
            timeout=10,
        )
        if token_response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="GitHub token exchange failed")

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="GitHub access token missing")

        profile_response = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github+json"},
            timeout=10,
        )
        if profile_response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="GitHub profile lookup failed")

        profile = profile_response.json()
        email = profile.get("email")
        if not email:
            email_response = requests.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github+json"},
                timeout=10,
            )
            if email_response.status_code == 200:
                for item in email_response.json():
                    if item.get("primary") and item.get("verified"):
                        email = item.get("email")
                        break

        provider_id = str(profile.get("id"))
        display_name = profile.get("name") or profile.get("login") or "GitHub User"
        avatar_url = profile.get("avatar_url")
        username_hint = email.split("@")[0] if email else display_name

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unsupported provider")

    users = PDB.get_users(username=username_hint)
    if len(users) == 0:
        user = PDB.create_user(
            provider=provider,
            provider_id=provider_id,
            username_hint=username_hint,
            email=email,
            display_name=display_name,
            avatar_url=avatar_url,
        )
    else:
        user = users[0]
        user = PDB.update_user(username=user.get("username"), user=user, **{
            "display_name": display_name,
            "email": email,
            "avatar_url": avatar_url,
        })

    auth_token = _store_auth_session(user, provider, provider_id, email)
    callback_target = pending["callback_url"]
    device_code = pending.get("device_code")
    payload = {
        "provider": provider,
        "username": user.get("username", ""),
        "display_name": display_name,
        "email": email or "",
    }

    if device_code:
        _store_device_authorization(device_code, auth_token, user, provider)

    if not _is_web_callback(callback_target):
        payload["token"] = auth_token

    redirect_target = _build_callback_redirect(callback_target, payload)
    response = RedirectResponse(redirect_target)

    secure_cookie = _cookie_secure(request)
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=auth_token,
        httponly=True,
        secure=secure_cookie,
        samesite=_cookie_samesite(secure_cookie),
        max_age=AUTH_SESSION_TTL_SECONDS,
        path="/",
    )
    return response


@app.get("/api/auth/session")
def auth_session(request: Request):
    """
    Uses Bearer token from the Authorization header or cookies to validate the user's session and return user info.
    """
    token = _extract_auth_token(request)
    user = _resolve_auth_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")

    session = _get_auth_session(token)
    provider = session.get("provider") if session else "api_key"
    return {"user": user, "provider": provider}


@app.post("/api/auth/device/start")
def auth_device_start():
    device_code = secrets.token_urlsafe(24)
    user_code = secrets.token_hex(4).upper()
    verification_uri = f"{_base_url()}/auth/login"
    verification_uri_complete = f"{verification_uri}?device_code={device_code}&user_code={user_code}"

    payload = {
        "status": "pending",
        "device_code": device_code,
        "user_code": user_code,
        "created_at": datetime.now(UTC).isoformat(),
    }
    REDIS.setex(f"lm:device:{device_code}", DEVICE_CODE_TTL_SECONDS, json.dumps(payload))
    REDIS.setex(f"lm:device_user:{user_code}", DEVICE_CODE_TTL_SECONDS, device_code)

    return {
        "device_code": device_code,
        "user_code": user_code,
        "verification_uri": verification_uri,
        "verification_uri_complete": verification_uri_complete,
        "interval": 3,
        "expires_in": DEVICE_CODE_TTL_SECONDS,
    }


@app.post("/api/auth/device/poll")
def auth_device_poll(data: DevicePollRequest):
    raw = REDIS.get(f"lm:device:{data.device_code}")
    if not raw:
        return {"status": "expired"}

    try:
        payload = json.loads(raw)
    except Exception:
        return {"status": "expired"}

    status_value = payload.get("status", "pending")
    if status_value != "approved":
        return {"status": "pending"}

    REDIS.delete(f"lm:device:{data.device_code}")
    user_code = payload.get("user_code")
    if user_code:
        REDIS.delete(f"lm:device_user:{user_code}")

    return {
        "status": "approved",
        "token": payload.get("token"),
        "user": payload.get("user"),
        "provider": payload.get("provider"),
        "expires_in": REDIS.ttl(f"lm:session:{payload.get('token')}") or 0,
    }


@app.post("/api/auth/logout")
def auth_logout(request: Request):
    token = _extract_auth_token(request)
    _delete_auth_session(token)
    response = JSONResponse({"status": "success"})
    response.delete_cookie(key=AUTH_COOKIE_NAME, path="/")
    return response


@app.get("/api/auth/api-keys")
def auth_api_keys(request: Request):
    token = _extract_auth_token(request)
    user = _resolve_auth_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    keys = PDB.list_api_keys_for_user(user.get("username"))
    return {"keys": keys}


@app.post("/api/auth/api-keys")
def auth_api_keys_create(request: Request, payload: APIKeyCreateRequest):
    token = _extract_auth_token(request)
    user = _resolve_auth_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    key = PDB.create_api_key_for_user(user.get("username"), payload.label or "No Label")
    return key


@app.delete("/api/auth/api-keys/{key_id}")
def auth_api_keys_delete(key_id: str, request: Request):
    token = _extract_auth_token(request)
    user = _resolve_auth_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    removed = PDB.revoke_api_key_for_user(user.get("username"), key_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found")

    return {"status": "success"}


@app.get("/api")
def read_root():
    return {"Welcome!": "Log Machine API is running!"}


@app.get("/api/rooms")
async def list_rooms(request: Request):
    user = _require_auth_user(request)
    rooms = await PDB.list_rooms_for_user(user.get("username"))
    return {"rooms": rooms}


@app.post("/api/rooms")
def create_org_room(org_name: str | None = None, payload: OrgRoomCreateRequest = None, request: Request = None):
    user = _require_auth_user(request)
    try:
        if org_name:
            room = PDB.create_org_room(
                org_name=org_name,
                actor_username=user.get("username"),
                room_id=payload.room,
                visibility=(payload.visibility or "private").strip().lower(),
            )
        else:
            room = PDB.create_room(room_id=payload.room, owner_type="user", owner_id=user.get("username"), visibility=(payload.visibility or "private").strip().lower())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    if not room:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to create this room")
    return {"status": "success", "room": room}


@app.get("/api/rooms/{room_id}")
def room_details(room_id: str, request: Request):
    room = PDB.get_room(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    auth_token = _extract_auth_token(request)
    auth_user = _resolve_auth_user(auth_token)
    username = auth_user.get("username") if auth_user else None

    if not PDB.can_access_room(room_id, username=username, require_write=False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this room")

    return room


@app.put("/api/rooms/{room_id}/visibility")
def set_room_visibility(room_id: str, payload: RoomVisibilityRequest, request: Request):
    user = _require_auth_user(request)
    updated = PDB.set_room_visibility(room_id, user.get("username"), payload.visibility.strip().lower())
    if not updated:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update room visibility")
    room = PDB.get_room(room_id)
    return {"status": "success", "room": room}


@app.post("/api/rooms/{room_id}/share")
def share_room(room_id: str, payload: RoomShareRequest, request: Request):
    user = _require_auth_user(request)
    shared = PDB.share_room_with_user(
        room_id=room_id,
        actor_username=user.get("username"),
        target_username=payload.username,
        can_write=payload.can_write,
    )
    if not shared:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to share this room")
    room = PDB.get_room(room_id)
    return {"status": "success", "room": room}


@app.delete("/api/rooms/{room_id}/share/{target_username}")
def unshare_room(room_id: str, target_username: str, request: Request):
    user = _require_auth_user(request)
    removed = PDB.unshare_room_with_user(room_id, user.get("username"), target_username)
    if not removed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to unshare this room")
    room = PDB.get_room(room_id)
    return {"status": "success", "room": room}


@app.post("/api/orgs")
def create_org(payload: OrgCreateRequest, request: Request):
    user = _require_auth_user(request)
    try:
        org = PDB.create_organisation(payload.name, user.get("username"))
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return {"status": "success", "organisation": org}


@app.get("/api/orgs")
def list_orgs(request: Request):
    user = _require_auth_user(request)
    orgs = PDB.list_organisations_for_user(user.get("username"))
    return {"organisations": orgs}


@app.get("/api/orgs/{org_name}")
def org_details(org_name: str, request: Request):
    user = _require_auth_user(request)
    if not PDB.is_org_member(org_name, user.get("username")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this organisation")

    org = PDB.get_organisation(org_name)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")
    rooms = PDB.list_org_rooms(org_name)
    return {"organisation": org, "rooms": rooms}


@app.post("/api/orgs/{org_name}/members")
def add_org_member(org_name: str, payload: OrgMemberRequest, request: Request):
    user = _require_auth_user(request)
    added = PDB.add_org_member(org_name, user.get("username"), payload.username, payload.role)
    if not added:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to add members")
    return {"status": "success", "organisation": PDB.get_organisation(org_name)}


@app.put("/api/orgs/{org_name}/members/{member_username}")
def update_org_member_role(org_name: str, member_username: str, payload: OrgMemberRoleRequest, request: Request):
    user = _require_auth_user(request)
    updated = PDB.set_org_member_role(org_name, user.get("username"), member_username, payload.role)
    if not updated:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update this role")
    return {"status": "success", "organisation": PDB.get_organisation(org_name)}


@app.delete("/api/orgs/{org_name}/members/{member_username}")
def remove_org_member(org_name: str, member_username: str, request: Request):
    user = _require_auth_user(request)
    removed = PDB.remove_org_member(org_name, user.get("username"), member_username)
    if not removed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to remove this member")
    return {"status": "success", "organisation": PDB.get_organisation(org_name)}


@app.post("/api/logs")
async def log_entry(log: LogEntry, room: str = None, request: Request = None) -> Dict[str, str]:
    """
    Endpoint to receive log entries and process them.
    """
    if not room:
        return {"status": "error", "message": "Room ID is required"}

    auth_token = _extract_auth_token(request) if request else None
    auth_user = _resolve_auth_user(auth_token)
    if not auth_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is required to post logs to this endpoint. Try: login()")

    if not PDB.can_access_room(room, username=auth_user.get("username"), require_write=True):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have write access to this room")

    try:
        payload = {
            "room": room,
            "log": log,
            "user": auth_user.get("username", log.user),
            "timestamp": datetime.now(UTC).isoformat()
        }

        log = PDB.add_log(room, payload)
        await sio.emit("log", log, room=room)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to process log entry: {e}")


@app.get("/api/logs")
def get_logs_via_http(room_id: str, request: Request):
    """
    Gets log entries in a room
    :param room_id: the room from which the logs live
    :return: list of log entries
    """
    auth_token = _extract_auth_token(request) if request else None
    auth_user = _resolve_auth_user(auth_token)
    username = auth_user.get("username") if auth_user else None

    if not PDB.can_access_room(room_id, username=username, require_write=False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this room")

    return PDB.get_logs(room_id)


@sio.event
async def connect(sid, environ, auth):
    token = auth.get("token") if auth else None
    if not token:
        cookie_extract = environ.get("HTTP_COOKIE", "").split("; ")
        cookies = {c.split("=", 1)[0]: c.split("=", 1)[1] for c in cookie_extract if "=" in c}
        token = cookies.get(AUTH_COOKIE_NAME)

    auth_user = _resolve_auth_user(token)
    if token and not auth_user:
        return False

    else:
        await sio.save_session(sid, {"auth_user": auth_user})


@sio.event
async def disconnect(sid):
    username = SID_TO_USER.pop(sid, None)
    room_ids = list(SID_TO_ROOMS.pop(sid, set()))
    for room_id in room_ids:
        if username and room_id in ROOM_VIEWERS:
            ROOM_VIEWERS[room_id].discard(username)
            if not ROOM_VIEWERS[room_id]:
                ROOM_VIEWERS.pop(room_id, None)
        await _emit_room_presence(room_id)


@sio.event
async def join(sid, data: dict) -> None:
    room_id = data.get("room")
    if not room_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room ID is required")

    session = await sio.get_session(sid)
    username = session.get("auth_user", {}).get("username")
    if not PDB.can_access_room(room_id, username=username, require_write=False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this room")

    await sio.enter_room(sid, str(room_id))
    SID_TO_ROOMS[sid].add(str(room_id))
    if username:
        SID_TO_USER[sid] = username
        ROOM_VIEWERS[str(room_id)].add(username)

    await _emit_room_presence(str(room_id))


@sio.event
async def leave(sid, data: dict) -> None:
    room_id = data.get("room")
    if not room_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room ID is required")

    session = await sio.get_session(sid)
    username = session.get("auth_user", {}).get("username")
    if not PDB.can_access_room(room_id, username=username, require_write=False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this room")

    await sio.leave_room(sid, str(room_id))
    SID_TO_ROOMS[sid].discard(str(room_id))
    if username and room_id in ROOM_VIEWERS:
        ROOM_VIEWERS[room_id].discard(username)
        if not ROOM_VIEWERS[room_id]:
            ROOM_VIEWERS.pop(room_id, None)

    await _emit_room_presence(str(room_id))


@sio.event
async def log(sid, payload: dict) -> dict | None:
    room_id = str(payload.get("room")) if "room" in payload else None
    if not room_id:
        return {"status": "error", "message": "Room ID is required"}

    log = payload.get("data", {})
    session = await sio.get_session(sid)
    auth_user = session.get("auth_user")
    if not await PDB.can_access_room(room_id, username=auth_user.get("username"), require_write=True):
        return {"status": "error", "message": "You do not have write access to this room"}

    LogEntry.model_validate(log)
    try:
        log = PDB.add_log(room_id, log)
        await sio.emit("log", log, room=room_id, skip_sid=sid)
        return {"status": "queued"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to process log entry: {e}"}


@sio.event
async def get_logs(sid: str, conf: dict = {}) -> dict | None:
    """
    Fetch logs for a specific room.
    :param sid: Socket ID of the client
    :param room_id: ID of the room to fetch logs from
    """
    room_id = conf.get("room", None)
    if not room_id:
        return {"status": "error", "message": "Room ID is required"}

    room = PDB.get_room(room_id)
    if not room:
        return {"status": "error", "message": f"Room {room_id} does not exist"}

    session = await sio.get_session(sid)
    auth_user = session.get("auth_user") if session else None
    username = auth_user.get("username") if auth_user else None
    if not await PDB.can_access_room(room_id, username=username, require_write=False):
        return {"status": "error", "message": "You do not have access to this room"}

    logs = PDB.get_logs(room_id)
    await sio.emit("logs", logs, to=sid)


@sio.event
async def clear_logs(sid: str, room_id: str) -> dict:
    """
    Clear logs for a specific room.
    :param sid: Socket ID of the client
    :param room_id: ID of the room to clear logs from
    """
    try:
        if not room_id:
            return {"status": "error", "message": "Room ID is required"}

        room = PDB.get_room(room_id)
        if not room:
            return {"status": "error", "message": f"Room {room_id} does not exist"}

        session = await sio.get_session(sid)
        auth_user = session.get("auth_user") if session else None
        username = auth_user.get("username") if auth_user else None
        if not PDB.can_access_room(room_id, username=username, require_write=True):
            return {"status": "error", "message": "You do not have write access to this room"}

        PDB.clear_logs(room_id, username)
        await sio.emit("logs_cleared", {"room": room_id, "username": username}, skip_sid=sid, room=room_id)
        return {"status": "success", "message": "Logs cleared successfully"}
    except Exception as e:
        await sio.emit("error", f"Failed to clear logs: {e}", to=sid)
        return {"status": "error", "message": f"Failed to clear logs: {e}"}
