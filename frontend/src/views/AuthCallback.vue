<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { auth } from '@/stores/auth'

const route = useRoute()
const status = ref('Completing sign in...')
const errorMessage = ref('')

const username = computed(() => (route.query.username || route.query.display_name || 'unknown').toString())
const provider = computed(() => (route.query.provider || '').toString())

onMounted(async () => {
  try {
    if (auth.state.loading) auth.state.loading = false
    await auth.bootstrapSession()

    const user = auth.state.user
    if (!user?.username) {
      errorMessage.value = 'Authentication session was not established.'
      status.value = 'Authentication failed.'
      return
    }

    const session = {
      username: user.username,
      provider: provider.value || auth.state.provider,
      email: user.email || (route.query.email || '').toString(),
    }

    if (window.opener && !window.opener.closed) {
      window.opener.postMessage({ type: 'logmachine-auth', ...session }, window.location.origin)
    }

    status.value = `Signed in as ${user.username || username.value}`
  } catch {
    errorMessage.value = 'Unable to validate the session cookie.'
    status.value = 'Authentication failed.'
  }
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-950 via-slate-900 to-cyan-950 px-4 py-12 text-white">
    <div class="mx-auto flex min-h-[calc(100vh-6rem)] max-w-3xl items-center">
      <div class="w-full rounded-[2rem] border border-white/10 bg-white/5 p-10 shadow-2xl shadow-black/30 backdrop-blur">
        <p class="inline-flex rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-1 text-sm font-medium text-emerald-200">Authentication complete</p>
        <h1 class="mt-6 text-4xl font-bold md:text-5xl">{{ status }}</h1>
        <p v-if="provider" class="mt-4 text-slate-300">Provider: {{ provider }}</p>
        <p v-if="errorMessage" class="mt-6 rounded-2xl border border-rose-400/30 bg-rose-400/10 px-4 py-3 text-rose-200">{{ errorMessage }}</p>

        <div v-else class="mt-8 rounded-2xl border border-white/10 bg-slate-900/80 p-5">
          <p class="text-sm uppercase tracking-[0.2em] text-slate-400">Secure session</p>
          <p class="mt-2 text-sm text-cyan-200">Authenticated via HTTP-only cookie.</p>
          <p class="mt-4 text-sm text-slate-400">
            Your browser session is now managed by the server and attached automatically on API requests.
          </p>
        </div>

        <div class="mt-8 flex flex-col gap-3 sm:flex-row">
          <router-link to="/logs" class="inline-flex items-center justify-center rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400">
            Go to logs
          </router-link>
          <router-link to="/auth/login" class="inline-flex items-center justify-center rounded-xl border border-white/15 px-5 py-3 font-semibold text-white transition hover:bg-white/10">
            Sign in again
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>