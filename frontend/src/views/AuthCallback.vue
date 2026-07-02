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
  <div class="min-h-screen bg-[#fafafa] dark:bg-[#000000] text-[#171717] dark:text-[#ffffff] px-4 py-12">
    <div class="mx-auto flex min-h-[calc(100vh-6rem)] max-w-3xl items-center">
      <div class="w-full rounded-md border border-neutral-200 dark:border-neutral-800 bg-[#ffffff] dark:bg-[#0a0a0a] p-10 shadow-sm">
        <p class="inline-flex rounded-md border border-neutral-200 dark:border-neutral-800 bg-neutral-100 dark:bg-neutral-900 px-4 py-1 text-sm font-medium text-neutral-600 dark:text-neutral-400">Authentication complete</p>
        <h1 class="mt-6 text-4xl font-bold md:text-5xl text-[#171717] dark:text-[#ffffff]">{{ status }}</h1>
        <p v-if="provider" class="mt-4 text-neutral-500 dark:text-neutral-400">Provider: {{ provider }}</p>
        <p v-if="errorMessage" class="mt-6 rounded-md border border-rose-500/30 bg-[#ffffff] dark:bg-[#0a0a0a] px-4 py-3 text-sm text-rose-600 dark:text-rose-400">{{ errorMessage }}</p>

        <div v-else class="mt-8 rounded-md border border-neutral-200 dark:border-neutral-800 bg-neutral-50/50 dark:bg-neutral-900/30 p-5">
          <p class="text-sm uppercase tracking-[0.2em] text-[#171717] dark:text-[#ffffff] font-semibold">Secure session</p>
          <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">Authenticated via HTTP-only cookie.</p>
          <p class="mt-4 text-sm text-neutral-500 dark:text-neutral-400">
            Your browser session is now managed by the server and attached automatically on API requests.
          </p>
        </div>

        <div class="mt-8 flex flex-col gap-3 sm:flex-row">
          <router-link to="/logs" class="inline-flex items-center justify-center rounded-md bg-[#171717] text-[#ffffff] dark:bg-[#ffffff] dark:text-[#000000] hover:bg-neutral-800 dark:hover:bg-neutral-100 px-5 py-3 font-semibold transition-colors">
            Go to logs
          </router-link>
          <router-link to="/auth/login" class="inline-flex items-center justify-center rounded-md border border-neutral-200 dark:border-neutral-800 bg-transparent text-[#171717] dark:text-[#ffffff] hover:bg-neutral-50 dark:hover:bg-neutral-900 px-5 py-3 font-semibold transition-colors">
            Sign in again
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>