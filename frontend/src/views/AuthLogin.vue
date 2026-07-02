<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { globals } from '@/stores/global'
import { auth } from '@/stores/auth'
import router from '@/router'

const route = useRoute()
const availableProviderIds = ref(new Set())
const loading = ref(true)
const errorMessage = ref('')
const enteredUserCode = ref('')

const providerCards = [
  {
    id: 'google',
    name: 'Google',
    description: 'Use your Google account',
    accent: 'from-rose-500 to-orange-500',
  },
  {
    id: 'github',
    name: 'GitHub',
    description: 'Use your GitHub account',
    accent: 'from-slate-700 to-slate-950',
  },
]

const defaultCallbackUrl = window.location.origin + router.resolve({ name: 'auth-callback' }).href
const callbackUrl = computed(() => (route.query.callback_url || route.query.callback || route.query.redirect_uri || defaultCallbackUrl).toString())
const deviceCode = computed(() => (route.query.device_code || '').toString())
const userCode = computed(() => (route.query.user_code || '').toString())

const visibleProviders = computed(() => providerCards.map((provider) => ({
  ...provider,
  available: availableProviderIds.value.has(provider.id),
})))

function startLogin(providerId) {
  auth.signOut() // Clear any existing session before starting a new login flow
  const url = new URL(`${globals.apiUrl}/auth/start/${providerId}`)
  url.searchParams.set('callback_url', callbackUrl.value)
  if (deviceCode.value) {
    url.searchParams.set('device_code', deviceCode.value)
  }
  const normalizedCode = (enteredUserCode.value || userCode.value || '').trim().toUpperCase()
  if (normalizedCode) {
    url.searchParams.set('user_code', normalizedCode)
  }
  window.location.assign(url.toString())
}

onMounted(async () => {
  enteredUserCode.value = userCode.value

  try {
    const response = await fetch(`${globals.apiUrl}/auth/providers`, { credentials: 'include' })
    const payload = await response.json()
    availableProviderIds.value = new Set((payload.providers || []).map((provider) => provider.id))
  } catch (error) {
    errorMessage.value = 'Unable to load login providers right now.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-[#fafafa] dark:bg-[#000000] text-[#171717] dark:text-[#ffffff] px-4 py-10">
    <div class="mx-auto flex min-h-[calc(100vh-5rem)] max-w-5xl items-center">
      <div class="grid w-full grid-cols-1 gap-8 lg:grid-cols-[1.1fr_0.9fr]">
        <section class="rounded-md border border-neutral-200 dark:border-neutral-800 bg-[#ffffff] dark:bg-[#0a0a0a] p-8 shadow-sm">
          <p class="mb-4 inline-flex rounded-md border border-neutral-200 dark:border-neutral-800 bg-neutral-100 dark:bg-neutral-900 px-4 py-1 text-sm font-medium text-neutral-600 dark:text-neutral-400">Secure sign in</p>
          <h1 class="max-w-xl text-4xl font-bold tracking-tight md:text-6xl text-[#171717] dark:text-[#ffffff]">
            Choose how you want to sign in.
          </h1>
          <p class="mt-6 max-w-xl text-lg leading-8 text-neutral-500 dark:text-neutral-400">
            LogMachine uses browser-based authentication so SDKs can hand off login to the web and receive a token back when the session completes.
          </p>

          <div class="mt-10 grid gap-4 sm:grid-cols-2">
            <button
              v-for="provider in visibleProviders"
              :key="provider.id"
              type="button"
              @click="startLogin(provider.id)"
              :disabled="!provider.available"
              class="group rounded-md border border-neutral-200 dark:border-neutral-800 bg-neutral-50 hover:bg-neutral-100/80 dark:bg-neutral-900 dark:hover:bg-neutral-800/80 p-5 text-left transition disabled:cursor-not-allowed disabled:opacity-60"
            >
              <div class="flex items-center justify-between gap-4">
                <div>
                  <p class="text-lg font-semibold text-[#171717] dark:text-[#ffffff]">Continue with {{ provider.name }}</p>
                  <p class="mt-1 text-sm text-neutral-500 dark:text-neutral-400">{{ provider.description }}</p>
                  <p v-if="!provider.available" class="mt-2 text-xs text-neutral-500 dark:text-neutral-400">Not configured yet in the backend</p>
                </div>
                <span class="text-2xl text-neutral-400 dark:text-neutral-500 transition-colors group-hover:text-black dark:group-hover:text-white">→</span>
              </div>
            </button>
          </div>

          <div class="mt-6 rounded-md border border-neutral-200 dark:border-neutral-800 bg-[#ffffff] dark:bg-[#0a0a0a] p-4" v-if="deviceCode || userCode">
            <p class="text-sm font-semibold text-[#171717] dark:text-[#ffffff]">Device code</p>
            <input
              v-model="enteredUserCode"
              type="text"
              maxlength="16"
              placeholder="Enter code, e.g. 1A2B3C4D"
              class="mt-3 w-full rounded-md border border-neutral-200 dark:border-neutral-700 bg-[#ffffff] dark:bg-[#000000] px-3 py-2 font-mono text-sm text-[#171717] dark:text-[#ffffff] outline-none focus:ring-1 focus:ring-neutral-400 focus:border-neutral-400"
            />
          </div>

          <div v-if="loading" class="mt-6 text-sm text-neutral-500 dark:text-neutral-400">Loading providers...</div>
          <div v-else-if="errorMessage" class="mt-6 rounded-md border border-rose-500/30 bg-[#ffffff] dark:bg-[#0a0a0a] px-4 py-3 text-sm text-rose-600 dark:text-rose-400">
            {{ errorMessage }}
          </div>
          <!-- <p class="mt-8 text-sm text-slate-400">
            Callback URL: <span class="break-all text-slate-200">{{ callbackUrl }}</span>
          </p> -->
          <p v-if="userCode" class="mt-3 text-sm text-neutral-600 dark:text-neutral-400">
            Device login code: <span class="font-mono font-semibold text-[#171717] dark:text-[#ffffff]">{{ userCode }}</span>
          </p>
        </section>

        <aside class="rounded-md border border-neutral-200 dark:border-neutral-800 bg-neutral-50/50 dark:bg-neutral-900/30 p-8 shadow-none">
          <h2 class="text-2xl font-semibold text-[#171717] dark:text-[#ffffff]">What happens next</h2>
          <ol class="mt-6 space-y-4 text-neutral-500 dark:text-neutral-400">
            <li class="rounded-md border border-neutral-200/60 dark:border-neutral-800/60 bg-[#ffffff] dark:bg-[#000000] p-4 text-sm">1. Pick Google or GitHub in this screen.</li>
            <li class="rounded-md border border-neutral-200/60 dark:border-neutral-800/60 bg-[#ffffff] dark:bg-[#000000] p-4 text-sm">2. Finish the browser sign-in flow.</li>
            <li class="rounded-md border border-neutral-200/60 dark:border-neutral-800/60 bg-[#ffffff] dark:bg-[#000000] p-4 text-sm">3. The backend sets a secure HTTP-only session cookie.</li>
            <li class="rounded-md border border-neutral-200/60 dark:border-neutral-800/60 bg-[#ffffff] dark:bg-[#000000] p-4 text-sm">4. The web app uses that cookie to authenticate API calls automatically.</li>
          </ol>

          <div class="mt-8 rounded-md border border-neutral-200 dark:border-neutral-800 bg-neutral-100 dark:bg-neutral-900 p-5 text-sm text-neutral-600 dark:text-neutral-400">
            This page is provider-agnostic in the SDK. The provider choice lives here in the browser UI, not in the SDK API.
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>
