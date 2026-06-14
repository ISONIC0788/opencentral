import { globals } from './global'

async function parseJsonSafe(response) {
  try {
    return await response.json()
  } catch {
    return {}
  }
}

export async function apiFetch(path, options = {}) {
  const response = await fetch(`${globals.apiUrl}${path}`, {
    credentials: 'include',
    ...options,
    headers: {
      ...(options.headers || {}),
    },
  })

  if (!response.ok) {
    const payload = await parseJsonSafe(response)
    const detail = payload.detail || payload.message || `Request failed: ${response.status}`
    throw Object.assign(new Error(detail), { status: response.status, detail })
  }

  return parseJsonSafe(response)
}

export function apiGet(path) {
  return apiFetch(path, { method: 'GET' })
}

export function apiPost(path, body) {
  return apiFetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body || {}),
  })
}

export function apiPut(path, body) {
  return apiFetch(path, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body || {}),
  })
}

export function apiDelete(path) {
  return apiFetch(path, { method: 'DELETE' })
}
