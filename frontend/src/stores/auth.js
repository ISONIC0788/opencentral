import { computed, reactive } from 'vue'
import { globals } from './global'

const state = reactive({
  user: null,
  provider: '',
  loaded: false,
  loading: false,
})

async function bootstrapSession() {
  if (state.loading) {
    return
  }

  state.loading = true
  try {
    const response = await fetch(`${globals.apiUrl}/auth/session`, {
      method: 'GET',
      credentials: 'include',
    })

    if (!response.ok) {
      state.user = null
      state.provider = ''
      return
    }

    const payload = await response.json()
    state.user = payload.user || null
    state.provider = payload.provider || ''
  } catch {
    state.user = null
    state.provider = ''
  } finally {
    state.loading = false
    state.loaded = true
  }
}

async function signOut() {
  try {
    await fetch(`${globals.apiUrl}/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    })
  } catch {
    // no-op; local auth state is still cleared below
  }

  state.user = null
  state.provider = ''
  state.loaded = true
}

function setSession(user, provider = '') {
  state.user = user
  state.provider = provider
  state.loaded = true
}

export const auth = {
  state,
  isAuthenticated: computed(() => Boolean(state.user?.username)),
  bootstrapSession,
  signOut,
  setSession,
}
