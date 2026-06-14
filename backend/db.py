import hashlib
import os
import re
import secrets
import traceback
from datetime import datetime, UTC

import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from psycopg.types.json import Json

from logger import logger


class DB:
    """
    PostgreSQL-backed data layer using JSONB payload columns.
    """

    def __init__(self, db_name="central"):
        self.db_name = db_name
        self.db_url = os.getenv("DATABASE_URL") or f"postgresql:///{db_name}"
        self.rag_embedding_dim = int(os.getenv("RAG_EMBEDDING_DIM", "256"))
        self.client = None

    def connect(self):
        """
        Connect to PostgreSQL and return a reusable connection.
        """
        if self.client and not self.client.closed:
            return self.client

        try:
            self.client = psycopg.connect(self.db_url, row_factory=dict_row, autocommit=True)
            return self.client
        except Exception as e:
            logger.error(f"Could not connect to PostgreSQL: {e}")
            return None

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.client is not None:
            try:
                self.client.close()
                logger.success("Database connection closed successfully.")
            except Exception:
                logger.error(f"Error closing database connection: {traceback.format_exc()}")
        else:
            logger.warning("No active database connection to close.")

    def _user_row_to_dict(self, row):
        if not row:
            return None

        merged = {
            "username": row.get("username"),
            **(row.get("data") or {}),
        }
        merged.setdefault("updated_at", row.get("updated_at"))
        return merged

    def list_owned_organisations(self, username: str) -> list[dict]:
        orgs = self.list_organisations_for_user(username)
        owned = []
        for org in orgs:
            role = self._org_member_role(org.get("members") or [], username)
            if role == "owner":
                owned.append(org)
        return owned

    def _is_admin_username(self, username: str | None) -> bool:
        if not username:
            return False
        users = self.get_users(username=username)
        if not users:
            return False
        user_type = users[0].get("type")
        return user_type == "admin"

    def _extract_shared_access(self, shared_with: list, username: str, require_write: bool) -> bool:
        for entry in shared_with or []:
            if isinstance(entry, str) and entry == username:
                return not require_write
            if not isinstance(entry, dict):
                continue
            if entry.get("username") != username:
                continue
            if not require_write:
                return True
            return bool(entry.get("can_write", False))
        return False

    def _org_has_member(self, members: list, username: str) -> bool:
        for member in members or []:
            if isinstance(member, str) and member == username:
                return True
            if isinstance(member, dict) and (member.get("username") == username or member.get("user") == username):
                return True
        return False

    def _org_member_role(self, members: list, username: str) -> str | None:
        for member in members or []:
            if isinstance(member, str) and member == username:
                return "developer"
            if not isinstance(member, dict):
                continue
            if member.get("username") == username or member.get("user") == username:
                return (member.get("role") or "developer").strip().lower()
        return None

    def get_users(self, **kwargs) -> list[dict]:
        conn = self.connect()
        if conn is None:
            return []

        clauses = []
        params = []
        for key, value in kwargs.items():
            if key == "username":
                clauses.append("username = %s")
                params.append(value)
            else:
                clauses.append("data ->> %s = %s")
                params.extend([key, str(value)])

        where_sql = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        with conn.cursor() as cur:
            cur.execute(f"SELECT username, data, updated_at FROM users{where_sql}", tuple(params))
            return [self._user_row_to_dict(row) for row in cur.fetchall()]

    def create_organisation(self, name: str, owner_username: str, max_rooms: int = 100):
        clean_name = (name or "").strip()
        if not clean_name:
            raise ValueError("Organisation name is required")

        if self.list_owned_organisations(owner_username):
            raise ValueError("Only one owned organisation is allowed per user")

        conn = self.connect()
        if conn is None:
            raise RuntimeError("Database connection unavailable")

        members = [{"username": owner_username, "role": "owner", "joined_at": datetime.now(UTC).isoformat()}]
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO organisations (name, members, max_rooms, updated_at)
                VALUES (%s, %s::jsonb, %s, NOW())
                ON CONFLICT (name) DO NOTHING
                """,
                (clean_name, Json(members), int(max_rooms)),
            )

        return self.get_organisation(clean_name)

    def get_organisation(self, name: str):
        conn = self.connect()
        if conn is None:
            return None

        with conn.cursor() as cur:
            cur.execute(
                "SELECT name, members, max_rooms, updated_at FROM organisations WHERE name = %s LIMIT 1",
                (name,),
            )
            row: dict = cur.fetchone()
            if not row:
                return None
            return {
                "name": row.get("name"),
                "members": row.get("members") or [],
                "max_rooms": int(row.get("max_rooms") or 0),
                "updated_at": row.get("updated_at"),
            }

    def list_organisations_for_user(self, username: str):
        conn = self.connect()
        if conn is None:
            return []

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT name, members, max_rooms, updated_at
                FROM organisations
                WHERE EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements(members) m
                    WHERE m->>'username' = %s
                )
                ORDER BY updated_at DESC;
                """,
                (username,),
            )
            rows: list[dict] = cur.fetchall() or []

        return [
            {
                "name": row.get("name"),
                "members": row.get("members") or [],
                "max_rooms": int(row.get("max_rooms") or 0),
                "updated_at": row.get("updated_at"),
            }
            for row in rows
        ]

    def is_org_member(self, org_name: str, username: str, require_admin: bool = False, require_write: bool = False) -> bool:
        org = self.get_organisation(org_name)
        if not org:
            return False

        role = self._org_member_role(org.get("members") or [], username)
        if not role:
            return False

        if require_admin:
            return role in {"owner", "admin"}

        if require_write:
            return role in {"owner", "admin", "developer"}

        return True

    def add_org_member(self, org_name: str, actor_username: str, target_username: str, role: str = "developer") -> bool:
        if not self.is_org_member(org_name, actor_username, require_admin=True):
            return False

        role = (role or "developer").strip().lower()
        if role not in {"admin", "developer", "viewer"}:
            raise ValueError("Invalid org role")

        org = self.get_organisation(org_name)
        if not org:
            return False

        members = org.get("members") or []
        updated = []
        found = False
        for member in members:
            if isinstance(member, str):
                if member == target_username:
                    updated.append({"username": target_username, "role": role, "joined_at": datetime.now(UTC).isoformat()})
                    found = True
                else:
                    updated.append(member)
                continue

            if isinstance(member, dict) and (member.get("username") == target_username or member.get("user") == target_username):
                member["username"] = target_username
                member["role"] = role
                updated.append(member)
                found = True
            else:
                updated.append(member)

        if not found:
            updated.append({"username": target_username, "role": role, "joined_at": datetime.now(UTC).isoformat()})

        conn = self.connect()
        if conn is None:
            return False

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE organisations SET members = %s::jsonb, updated_at = NOW() WHERE name = %s",
                (Json(updated), org_name),
            )
        return True

    def set_org_member_role(self, org_name: str, actor_username: str, target_username: str, role: str) -> bool:
        if not self.is_org_member(org_name, actor_username, require_admin=True):
            return False

        role = (role or "").strip().lower()
        if role not in {"admin", "developer", "viewer"}:
            raise ValueError("Invalid org role")

        org = self.get_organisation(org_name)
        if not org:
            return False

        members = org.get("members") or []
        updated = []
        changed = False
        for member in members:
            if isinstance(member, dict) and (member.get("username") == target_username or member.get("user") == target_username):
                if member.get("role") == "owner":
                    updated.append(member)
                    continue
                member["role"] = role
                updated.append(member)
                changed = True
            elif isinstance(member, str) and member == target_username:
                updated.append({"username": target_username, "role": role, "joined_at": datetime.now(UTC).isoformat()})
                changed = True
            else:
                updated.append(member)

        if not changed:
            return False

        conn = self.connect()
        if conn is None:
            return False

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE organisations SET members = %s::jsonb, updated_at = NOW() WHERE name = %s",
                (Json(updated), org_name),
            )
        return True

    def remove_org_member(self, org_name: str, actor_username: str, target_username: str) -> bool:
        if not self.is_org_member(org_name, actor_username, require_admin=True):
            return False

        org = self.get_organisation(org_name)
        if not org:
            return False

        members = org.get("members") or []
        updated = []
        removed = False
        for member in members:
            if isinstance(member, dict) and (member.get("username") == target_username or member.get("user") == target_username):
                if member.get("role") == "owner":
                    updated.append(member)
                    continue
                removed = True
                continue
            if isinstance(member, str) and member == target_username:
                removed = True
                continue
            updated.append(member)

        if not removed:
            return False

        conn = self.connect()
        if conn is None:
            return False

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE organisations SET members = %s::jsonb, updated_at = NOW() WHERE name = %s",
                (Json(updated), org_name),
            )
        return True

    def list_org_rooms(self, org_name: str):
        conn = self.connect()
        if conn is None:
            return []

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT room, room_type, max_log_size, owner_type, owner_id, visibility,
                       COALESCE(shared_with, '[]'::jsonb) AS shared_with, updated_at
                FROM rooms
                WHERE owner_type = 'org' AND owner_id = %s
                ORDER BY updated_at DESC
                """,
                (org_name,),
            )
            rows: list[dict] = cur.fetchall() or []

        return [
            {
                "room": row.get("room"),
                "room_type": row.get("room_type", "standard"),
                "max_log_size": int(row.get("max_log_size") or 0),
                "owner_type": row.get("owner_type"),
                "owner_id": row.get("owner_id"),
                "visibility": row.get("visibility", "private"),
                "shared_with": row.get("shared_with") or [],
                "updated_at": row.get("updated_at"),
            }
            for row in rows
        ]

    def create_org_room(self, org_name: str, actor_username: str, room_id: str, visibility: str = "private"):
        if not self.is_org_member(org_name, actor_username, require_write=True):
            return None

        org = self.get_organisation(org_name)
        if not org:
            return None

        current_rooms = self.list_org_rooms(org_name)
        if len(current_rooms) >= int(org.get("max_rooms") or 0):
            raise ValueError("Organisation room limit reached")

        return self.create_room(
            room_id=room_id,
            owner_type="org",
            owner_id=org_name,
            room_type="premium",
            visibility=visibility,
        )

    def create_user(self, provider, provider_id, username_hint, email=None, display_name=None, avatar_url=None):
        conn = self.connect()
        if conn is None:
            raise RuntimeError("Database connection unavailable")

        with conn.cursor() as cur:
            base_username = username_hint or display_name or (email.split("@")[0] if email else provider)
            safe_username = re.sub(r"[^a-zA-Z0-9_]+", "_", base_username).strip("_") or provider
            username = safe_username

            while True:
                cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
                if not cur.fetchone():
                    break
                username = f"{safe_username}_{secrets.token_hex(2)}"

            data = {
                "provider": provider,
                "provider_id": str(provider_id),
                "email": email,
                "display_name": display_name,
                "avatar_url": avatar_url,
                "type": "standard", # default to standard user, can be updated to premium/admin later
                "api_keys": [],
                "updated_at": datetime.now(UTC).isoformat(),
            }
            cur.execute(
                "INSERT INTO users (username, data, updated_at) VALUES (%s, %s::jsonb, NOW())",
                (username, Json(data)),
            )

        self.create_room(room_id=username, owner_type="user", owner_id=username)
        return self._user_row_to_dict({"username": username, "data": data, "updated_at": datetime.now(UTC)})

    def update_user(self, username, **kwargs):
        conn = self.connect()
        if conn is None:
            raise RuntimeError("Database connection unavailable")

        with conn.cursor() as cur:
            cur.execute("SELECT data FROM users WHERE username = %s LIMIT 1", (username,))
            row = cur.fetchone()
            if not row:
                raise ValueError("User not found")

            data = row.get("data") or {}
            for key, value in kwargs.items():
                if key in ["username", "provider", "provider_id"] or (key == 'type' and data[key] == 'admin'):
                    continue
                data[key] = value
            data["updated_at"] = datetime.now(UTC).isoformat()

            cur.execute(
                "UPDATE users SET data = %s::jsonb, updated_at = NOW() WHERE username = %s",
                (Json(data), username),
            )

        return self._user_row_to_dict({"username": username, "data": data, "updated_at": datetime.now(UTC)})

    def create_api_key_for_user(self, username, label="Default key"):
        conn = self.connect()
        if conn is None:
            raise RuntimeError("Database connection unavailable")

        with conn.cursor() as cur:
            cur.execute("SELECT username, data FROM users WHERE username = %s LIMIT 1", (username,))
            row = cur.fetchone()
            if not row:
                raise ValueError("User not found")

            key_id = secrets.token_hex(8)
            api_key = f"lmk_{secrets.token_urlsafe(32)}"
            key_hash = hashlib.sha256(api_key.encode("utf-8")).hexdigest()
            key_preview = f"{api_key[:10]}...{api_key[-4:]}"
            created_at = datetime.now(UTC).isoformat()

            data = row.get("data") or {}
            api_keys = data.get("api_keys") or []
            api_keys.append(
                {
                    "id": key_id,
                    "label": label or f"Key {len(api_keys) + 1}",
                    "key_hash": key_hash,
                    "key_preview": key_preview,
                    "created_at": created_at,
                    "last_used_at": None,
                }
            )
            data["api_keys"] = api_keys
            data["updated_at"] = datetime.now(UTC).isoformat()

            cur.execute(
                "UPDATE users SET data = %s::jsonb, updated_at = NOW() WHERE username = %s",
                (Json(data), username),
            )

            return {
                "id": key_id,
                "label": label or f"Key {len(api_keys)}",
                "key_preview": key_preview,
                "created_at": created_at,
                "api_key": api_key,
            }

    def list_api_keys_for_user(self, username):
        conn = self.connect()
        if conn is None:
            return []

        with conn.cursor() as cur:
            cur.execute("SELECT data FROM users WHERE username = %s LIMIT 1", (username,))
            row = cur.fetchone()
            if not row:
                return []

            data = row.get("data") or {}
            keys = []
            for key in data.get("api_keys", []):
                keys.append(
                    {
                        "id": key.get("id"),
                        "label": key.get("label", "Default key"),
                        "key_preview": key.get("key_preview", ""),
                        "created_at": key.get("created_at"),
                        "last_used_at": key.get("last_used_at"),
                    }
                )
            return keys

    def revoke_api_key_for_user(self, username, key_id):
        conn = self.connect()
        if conn is None:
            return False

        with conn.cursor() as cur:
            cur.execute("SELECT data FROM users WHERE username = %s LIMIT 1", (username,))
            row = cur.fetchone()
            if not row:
                return False

            data = row.get("data") or {}
            api_keys = data.get("api_keys", [])
            filtered = [k for k in api_keys if k.get("id") != key_id]
            if len(filtered) == len(api_keys):
                return False

            data["api_keys"] = filtered
            data["updated_at"] = datetime.now(UTC).isoformat()
            cur.execute(
                "UPDATE users SET data = %s::jsonb, updated_at = NOW() WHERE username = %s",
                (Json(data), username),
            )
            return True

    def resolve_user_by_api_key(self, api_key):
        if not api_key:
            return None

        key_hash = hashlib.sha256(api_key.encode("utf-8")).hexdigest()
        conn = self.connect()
        if conn is None:
            return None

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT username, data, updated_at
                FROM users
                WHERE EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements(COALESCE(data->'api_keys', '[]'::jsonb)) k
                    WHERE k->>'key_hash' = %s
                )
                LIMIT 1
                """,
                (key_hash,),
            )
            row = cur.fetchone()
            if not row:
                return None

            data = row.get("data") or {}
            changed = False
            for key in data.get("api_keys", []):
                if key.get("key_hash") == key_hash:
                    key["last_used_at"] = datetime.now(UTC).isoformat()
                    changed = True
                    break

            if changed:
                data["updated_at"] = datetime.now(UTC).isoformat()
                cur.execute(
                    "UPDATE users SET data = %s::jsonb, updated_at = NOW() WHERE username = %s",
                    (Json(data), row["username"]),
                )

            return self._user_row_to_dict({"username": row["username"], "data": data, "updated_at": datetime.now(UTC)})

    async def list_rooms_for_user(self, username: str, limit: int = 200):
        if not username:
            return []

        conn = self.connect()
        if conn is None:
            return []

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT room, room_type, max_log_size, owner_type, owner_id, visibility,
                       COALESCE(shared_with, '[]'::jsonb) AS shared_with, updated_at
                FROM rooms
                ORDER BY updated_at DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows: list[dict] = cur.fetchall() or []

        rooms = []
        for row in rows:
            room_id = row.get("room")
            if not await self.can_access_room(room_id, username=username, require_write=False):
                continue

            can_write = await self.can_access_room(room_id, username=username, require_write=True)
            rooms.append(
                {
                    "room": room_id,
                    "room_type": row.get("room_type", "standard"),
                    "max_log_size": int(row.get("max_log_size") or 0),
                    "base_max_log_size": int(row.get("max_log_size") or 0),
                    "owner_type": row.get("owner_type"),
                    "owner_id": row.get("owner_id"),
                    "visibility": row.get("visibility", "private"),
                    "shared_with": row.get("shared_with") or [],
                    "can_write": bool(can_write),
                    "updated_at": row.get("updated_at"),
                }
            )

        return rooms

    def get_room(self, room_id):
        if not room_id:
            return None

        conn = self.connect()
        if conn is None:
            return None

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT room, room_type, max_log_size, owner_type, owner_id, visibility,
                       COALESCE(shared_with, '[]'::jsonb) AS shared_with, updated_at
                FROM rooms
                WHERE room = %s
                LIMIT 1
                """,
                (room_id,),
            )
            row: dict = cur.fetchone()
            if not row:
                return None

            return {
                "room": row.get("room"),
                "room_type": row.get("room_type", "standard"),
                "max_log_size": int(row.get("max_log_size") or 0),
                "base_max_log_size": int(row.get("max_log_size") or 0),
                "owner_type": row.get("owner_type"),
                "owner_id": row.get("owner_id"),
                "visibility": row.get("visibility", "private"),
                "shared_with": row.get("shared_with") or [],
                "updated_at": row.get("updated_at"),
            }

    async def can_access_room(self, room_id: str, username: str | None = None, require_write: bool = False) -> bool:
        room = self.get_room(room_id)
        if not room:
            return False

        if not require_write and room.get("visibility") == "public":
            return True

        if not username:
            return False

        if self._is_admin_username(username):
            return True

        owner_type = room.get("owner_type")
        owner_id = room.get("owner_id")

        if owner_type == "user" and owner_id == username:
            return True

        if owner_type == "org":
            conn = self.connect()
            if conn is None:
                return False
            with conn.cursor() as cur:
                cur.execute("SELECT members FROM organisations WHERE name = %s LIMIT 1", (owner_id,))
                org = cur.fetchone()
                if org:
                    role = self._org_member_role(org.get("members") or [], username)
                    if role and (not require_write or role in {"owner", "admin", "developer"}):
                        return True

        shared_with = room.get("shared_with") or []
        return self._extract_shared_access(shared_with, username, require_write)

    def create_room(self, room_id, owner_type="user", owner_id=None, room_type=None, visibility="private"):
        if self.get_room(room_id):
            return None

        if owner_type not in {"user", "org"}:
            raise ValueError("owner_type must be either 'user' or 'org'")

        if not owner_id:
            owner_id = room_id

        room_type_value = room_type or "standard"
        max_log_size = 5000 * 1024 * 1024
        conn = self.connect()
        if conn is None:
            raise RuntimeError("Database connection unavailable")

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO rooms (room, max_log_size, room_type, owner_type, owner_id, visibility, shared_with)
                VALUES (%s, %s, %s, %s, %s, %s, '[]'::jsonb)
                ON CONFLICT (room) 
                DO UPDATE SET 
                    max_log_size = EXCLUDED.max_log_size,
                    room_type = EXCLUDED.room_type,
                    owner_type = EXCLUDED.owner_type,
                    owner_id = EXCLUDED.owner_id,
                    visibility = EXCLUDED.visibility,
                    updated_at = NOW()
                RETURNING room, room_type, max_log_size, owner_type, owner_id, visibility, shared_with, updated_at;
                """,
                (room_id, max_log_size, room_type_value, owner_type, owner_id, visibility),
            )

            return cur.fetchone()

    def set_room_visibility(self, room_id: str, actor_username: str, visibility: str) -> bool:
        if visibility not in {"private", "public"}:
            raise ValueError("visibility must be 'private' or 'public'")

        room = self.get_room(room_id)
        if not room:
            return False

        if not self.can_access_room(room_id, actor_username, require_write=True):
            return False

        conn = self.connect()
        if conn is None:
            return False

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE rooms SET visibility = %s, updated_at = NOW() WHERE room = %s",
                (visibility, room_id),
            )
        return True

    def share_room_with_user(self, room_id: str, actor_username: str, target_username: str, can_write: bool = False) -> bool:
        if not target_username:
            return False

        if not self.can_access_room(room_id, actor_username, require_write=True):
            return False

        room = self.get_room(room_id)
        if not room:
            return False

        shared_with = room.get("shared_with") or []
        updated = []
        found = False
        for entry in shared_with:
            if isinstance(entry, str):
                if entry == target_username:
                    updated.append({"username": target_username, "can_write": bool(can_write)})
                    found = True
                else:
                    updated.append(entry)
                continue

            if isinstance(entry, dict) and entry.get("username") == target_username:
                entry["can_write"] = bool(can_write)
                updated.append(entry)
                found = True
            else:
                updated.append(entry)

        if not found:
            updated.append({"username": target_username, "can_write": bool(can_write)})

        conn = self.connect()
        if conn is None:
            return False

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE rooms SET shared_with = %s::jsonb, updated_at = NOW() WHERE room = %s",
                (Json(updated), room_id),
            )
        return True

    def unshare_room_with_user(self, room_id: str, actor_username: str, target_username: str) -> bool:
        if not self.can_access_room(room_id, actor_username, require_write=True):
            return False

        room = self.get_room(room_id)
        if not room:
            return False

        shared_with = room.get("shared_with") or []
        updated = []
        for entry in shared_with:
            if isinstance(entry, str) and entry == target_username:
                continue
            if isinstance(entry, dict) and entry.get("username") == target_username:
                continue
            updated.append(entry)

        conn = self.connect()
        if conn is None:
            return False

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE rooms SET shared_with = %s::jsonb, updated_at = NOW() WHERE room = %s",
                (Json(updated), room_id),
            )
        return True

    def delete_room(self, room_id):
        room = self.get_room(room_id)
        if not room:
            raise Exception(f"Room {room_id} does not exist. Cannot delete room.")

        conn = self.connect()
        if conn is None:
            return

        with conn.cursor() as cur:
            cur.execute("DELETE FROM rooms WHERE room = %s", (room_id,))

    def add_log(self, room_id: str, log_entry: dict, custom_expires_days: int | None = None):
        """
        Add a log entry to a room.
        - Uses room's retention policy by default
        - You can override expiry with custom_expires_days
        """
        conn = self.connect()
        if conn is None:
            raise RuntimeError("Database connection unavailable")

        with conn.cursor() as cur:
            try:
                cur.execute("""
                    SELECT room
                    FROM rooms
                    WHERE room = %s
                """, (room_id,))

                room = cur.fetchone()
                if not room:
                    raise ValueError("Room does not exist")

                if custom_expires_days is not None:
                    retention_days = int(custom_expires_days)
                else:
                    retention_days = 365

                # Insert log
                cur.execute("""
                    INSERT INTO logs (room, expires_at, username, avatar_url, level, module, message, timestamp, size_bytes)
                    VALUES (
                        %s, NOW() + (%s * INTERVAL '1 day'), %s,
                        (SELECT data ->> 'avatar_url' FROM users WHERE username = %s),
                        %s, %s, %s, %s,
                        octet_length(%s::text)
                    )
                    RETURNING username, avatar_url, level, module, message, timestamp::text
                """, (
                    room_id,
                    retention_days,
                    log_entry.get('user'), log_entry.get('user'),
                    log_entry.get('level'), log_entry.get('module'),
                    log_entry.get('message'), log_entry.get('timestamp'),
                    Json(log_entry)
                ))

                return cur.fetchone()

            except Exception as e:
                logger.error(f"Failed to add log to {room_id}: {e}")
                raise

    def clear_logs(self, room_id: str, username: str | None):
        conn = self.connect()
        if conn is None:
            raise RuntimeError("Database connection unavailable")

        with conn.cursor() as cur:
            if username:
                cur.execute("DELETE FROM logs WHERE room = %s AND username = %s", (room_id, username))
            else:
                cur.execute("DELETE FROM logs WHERE room = %s", (room_id,))

    def get_logs(self, room_id: str, page: int = 1, per_page: int = 100, 
             newest_first: bool = True, filters: dict | None = None):
        """
        Get logs with pagination + optional filtering (Premium rooms only for now)
        """
        if page < 1:
            page = 1
        offset = (page - 1) * per_page

        conn = self.connect()
        if conn is None:
            return {"logs": [], "total_logs": 0}

        with conn.cursor() as cur:
            # Get room type
            cur.execute("SELECT room_type FROM rooms WHERE room = %s", (room_id,))
            room = cur.fetchone()
            if not room:
                return {"logs": [], "total_logs": 0}


            # Build filter if premium + filters exist
            filter_sql = sql.SQL("")
            filter_params = []

            if filters:
                filter_sql, filter_params = self._build_filter_sql(filters)

            # Main query
            order_dir = sql.SQL("DESC") if newest_first else sql.SQL("ASC")
            base_query = sql.SQL("""
                    FROM logs
                    WHERE room = %s
                    AND expires_at > NOW()
                    {}
                """).format(filter_sql)

            data_query = sql.SQL("""SELECT username, level, module, message, timestamp::text, avatar_url {}
                                 ORDER BY timestamp {} LIMIT %s OFFSET %s""").format(base_query, order_dir)
            params = [room_id] + filter_params + [per_page, offset]
            cur.execute(data_query, params)
            logs = cur.fetchall()

            # Total count (with same filters)
            count_query = sql.SQL("SELECT COUNT(*) AS count {}").format(base_query)
            cur.execute(count_query, [room_id] + filter_params)
            total = cur.fetchone()['count']

            return {
                "logs": logs,
                "page": page,
                "per_page": per_page,
                "total_logs": total,
                "total_pages": (total + per_page - 1) // per_page if per_page > 0 else 0,
                "room": room_id,
                "filtered": bool(filters)
            }

    def _build_filter_sql(self, filters: dict) -> tuple[sql.SQL, list]:
        """
        Safely build WHERE clause + parameters
        """
        if not filters:
            return sql.SQL(""), []

        allowed_comparisons = {"=", "!=", "<", ">", "<=", ">=", "ILIKE", "in"}
        clauses = []
        params = []

        field_mapping = {
            "user": "username",
            "message": "message",
            "level": "level",
            "module": "module",
            "timestamp": "timestamp"
        }

        for field, (comp, value) in filters.items():
            column = field_mapping.get(field)
            if (not column) or (comp not in allowed_comparisons):
                continue

            column = sql.Identifier(column)
            if comp == "in" and isinstance(value, list):
                clauses.append(sql.SQL("{} = ANY(%s)").format(column))
                params.append(value)
            else:
                clauses.append(sql.SQL("{} {} %s").format(column, sql.SQL(comp)))
                params.append(value)

        if not clauses:
            return sql.SQL(""), []

        return sql.SQL(" AND {}").format(sql.SQL(" AND ").join(clauses)), params

    def _vector_literal(self, values):
        return "[" + ",".join(f"{float(v):.8f}" for v in values) + "]"

    def count_admins(self):
        """Count the number of admin users in the database."""
        conn = self.connect()
        if conn is None:
            return 0

        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total FROM users WHERE data ->> 'is_admin' = 'true'")
            row: dict = cur.fetchone() or {}
            return int(row.get("total", 0))

    def is_user_admin(self, username):
        """Check if a user is an admin."""
        conn = self.connect()
        if conn is None:
            return False

        with conn.cursor() as cur:
            cur.execute("SELECT data FROM users WHERE username = %s LIMIT 1", (username,))
            row: dict = cur.fetchone() or {}
            if not row:
                return False

            data = row.get("data") or {}
            return data.get("type") == "admin"

    def set_user_admin(self, username, is_admin=True):
        """Set or remove admin status for a user."""
        conn = self.connect()
        if conn is None:
            raise RuntimeError("Database connection unavailable")

        with conn.cursor() as cur:
            cur.execute("SELECT data FROM users WHERE username = %s LIMIT 1", (username,))
            row: dict = cur.fetchone() or {}
            if not row:
                raise ValueError(f"User {username} not found")

            data = row.get("data") or {}
            data["type"] = 'admin' if is_admin else 'regular'
            data["updated_at"] = datetime.now(UTC).isoformat()

            cur.execute(
                "UPDATE users SET data = %s::jsonb, updated_at = NOW() WHERE username = %s",
                (Json(data), username),
            )

    def create_local_admin_user(self, username):
        """Create a local admin user for bootstrap purposes."""
        conn = self.connect()
        if conn is None:
            raise RuntimeError("Database connection unavailable")

        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
            if cur.fetchone():
                cur.execute("SELECT data FROM users WHERE username = %s LIMIT 1", (username,))
                row: dict = cur.fetchone() or {}
                data = row.get("data") or {}
                data["type"] = "admin"
                data["updated_at"] = datetime.now(UTC).isoformat()
                cur.execute(
                    "UPDATE users SET data = %s::jsonb, updated_at = NOW() WHERE username = %s",
                    (Json(data), username),
                )
                return self._user_row_to_dict({"username": username, "data": data, "updated_at": datetime.now(UTC)})

            data = {
                "type": "admin",
                "display_name": "Administrator",
                "api_keys": [],
                "created_at": datetime.now(UTC).isoformat(),
                "updated_at": datetime.now(UTC).isoformat(),
            }

            cur.execute(
                "INSERT INTO users (username, data, updated_at) VALUES (%s, %s::jsonb, NOW())",
                (username, Json(data)),
            )

        self.create_room(room_id=username, owner_type="user", owner_id=username)
        return self._user_row_to_dict({"username": username, "data": data, "updated_at": datetime.now(UTC)})
