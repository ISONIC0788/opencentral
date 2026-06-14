<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { auth } from '@/stores/auth'

const router = useRouter()
const route = useRoute()

const isMenuOpen = ref(false)
const isDarkMode = ref(localStorage.getItem('theme') === 'dark')
const mobileMenuOpen = computed(() => isMenuOpen.value)
const authLoaded = computed(() => auth.state.loaded)
const isAuthenticated = computed(() => auth.isAuthenticated.value)
const authUser = auth.state.user

const navItems = ref([
  { label: 'Home', to: '/' },
  { label: 'Logs', to: '/logs' },
  { label: 'Docs', to: '/docs' },
  { label: 'Admin', to: '/admin', usable: authUser?.type === 'admin', adminOnly: true },
])

function applyTheme(theme) {
  localStorage.setItem('theme', theme)
  document.documentElement.classList.toggle('dark', theme === 'dark')
  isDarkMode.value = theme === 'dark'
}

function toggleDarkMode() {
  applyTheme(isDarkMode.value ? 'light' : 'dark')
}

function toggleMenu() {
  isMenuOpen.value = !isMenuOpen.value
}

function navigate(to) {
  isMenuOpen.value = false
  router.push(to)
}

async function signOut() {
  isMenuOpen.value = false
  await auth.signOut()
  router.push('/auth/login')
}

const storedTheme = localStorage.getItem('theme')
if (storedTheme) {
  document.documentElement.classList.toggle('dark', storedTheme === 'dark')
  isDarkMode.value = storedTheme === 'dark'
} else {
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
  applyTheme(prefersDark ? 'dark' : 'light')
}
</script>

<template>
  <nav class="border-b border-gray-200 bg-white/90 backdrop-blur dark:border-gray-700 dark:bg-gray-900/90">
    <div class="mx-auto flex max-w-screen-xl items-center justify-between gap-4 px-4 py-3 sm:px-6 lg:px-8">
      <RouterLink to="/" class="flex items-center gap-3 min-w-0">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="50" height="50" 
          class=""  
        >
          <!-- Machine body -->
          <rect class="dark:fill-[#2a2a2a] fill-[#f0ede6] dark:stroke-[#555] stroke-[#c8c5bc]" x="96" y="80" width="320" height="352" rx="40" stroke-width="2"/>

          <!-- Top bar -->
          <rect class="dark:fill-[#333] fill-[#e2dfd8]" x="96" y="80" width="320" height="76" rx="40"/>
          <rect class="dark:fill-[#333] fill-[#e2dfd8]" x="96" y="132" width="320" height="24"/>

          <!-- Bolts -->
          <circle class="dark:fill-[#555] fill-[#b8b5ad]" cx="136" cy="118" r="12"/>
          <circle class="dark:fill-[#555] fill-[#b8b5ad]" cx="376" cy="118" r="12"/>

          <!-- Screen -->
          <rect class="dark:fill-[#0f0f0f] fill-[#161616]" x="120" y="172" width="272" height="184" rx="12"/>

          <!-- Log level bars -->
          <!-- DEBUG gray -->
          <rect fill="#5F5E5A" x="138" y="190" width="52" height="16" rx="4"/>
          <rect fill="#2e2e2e" x="198" y="194" width="178" height="8" rx="3"/>

          <!-- INFO blue -->
          <rect fill="#185FA5" x="138" y="216" width="44" height="16" rx="4"/>
          <rect fill="#2e2e2e" x="190" y="220" width="168" height="8" rx="3"/>

          <!-- SUCCESS green -->
          <rect fill="#3B6D11" x="138" y="242" width="76" height="16" rx="4"/>
          <rect fill="#2e2e2e" x="222" y="246" width="148" height="8" rx="3"/>

          <!-- WARNING amber -->
          <rect fill="#854F0B" x="138" y="268" width="70" height="16" rx="4"/>
          <rect fill="#2e2e2e" x="216" y="272" width="152" height="8" rx="3"/>

          <!-- ERROR red -->
          <rect fill="#A32D2D" x="138" y="294" width="56" height="16" rx="4"/>
          <rect fill="#2e2e2e" x="202" y="298" width="160" height="8" rx="3"/>

          <!-- Cursor -->
          <rect fill="#1D9E75" x="138" y="318" width="14" height="20" rx="3"/>

          <!-- Bottom vents -->
          <rect class="dark:fill-[#555] fill-[#b8b5ad]" x="164" y="374" width="56" height="6" rx="3"/>
          <rect class="dark:fill-[#555] fill-[#b8b5ad]" x="292" y="374" width="56" height="6" rx="3"/>
          <rect class="dark:fill-[#555] fill-[#b8b5ad]" x="164" y="386" width="56" height="6" rx="3"/>
          <rect class="dark:fill-[#555] fill-[#b8b5ad]" x="292" y="386" width="56" height="6" rx="3"/>
        </svg>
        <div class="min-w-0">
          <p class="hidden sm:block truncate text-lg font-semibold text-gray-900 dark:text-white">Log Machine</p>
          <p class="hidden text-xs text-gray-500 dark:text-gray-400 md:block">Collaborative logging for distributed teams</p>
        </div>
      </RouterLink>

      <div class="hidden items-center gap-2 lg:flex">
        <RouterLink
          v-for="item in navItems"
          v-show="!item.adminOnly || item.usable"
          :key="item.to"
          :to="item.to"
          class="rounded-full px-4 py-2 text-sm font-medium transition-colors"
          :class="item.adminOnly ? 
            (route.path === item.to || route.path.startsWith('/admin') ? 'bg-purple-600 text-white dark:bg-purple-500' : 'text-gray-600 hover:bg-purple-50 hover:text-purple-700 dark:text-gray-300 dark:hover:bg-purple-900/30 dark:hover:text-purple-300') :
            (route.path === item.to || (item.to === '/docs' && route.path.startsWith('/docs')) ? 'bg-gray-900 text-white dark:bg-white dark:text-gray-900' : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-800 dark:hover:text-white')"
        >
          {{ item.label }}
        </RouterLink>
      </div>

      <div class="flex items-center gap-2">
        <RouterLink
          v-if="authLoaded && !isAuthenticated"
          to="/auth/login"
          class="hidden rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 px-4 py-2 text-sm font-semibold text-white transition hover:from-emerald-600 hover:to-teal-600 md:inline-flex"
        >
          Sign in
        </RouterLink>

        <RouterLink
          v-if="authLoaded && isAuthenticated"
          to="/profile"
          class="hidden rounded-full border border-emerald-300 bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-700 transition hover:bg-emerald-100 dark:border-emerald-500/40 dark:bg-emerald-500/10 dark:text-emerald-300 dark:hover:bg-emerald-500/20 md:inline-flex"
        >
          {{ authUser?.username || 'Profile' }}
        </RouterLink>

        <button
          v-if="authLoaded && isAuthenticated"
          type="button"
          @click="signOut"
          class="hidden rounded-full border border-rose-300 bg-rose-50 px-4 py-2 text-sm font-semibold text-rose-700 transition hover:bg-rose-100 dark:border-rose-500/40 dark:bg-rose-500/10 dark:text-rose-300 dark:hover:bg-rose-500/20 md:inline-flex"
        >
          Sign out
        </button>

        <!-- Dark Mode Toggle -->
        <div class="flex items-center gap-2">
          <!-- <span class="hidden md:block lg:block text-gray-800 dark:text-white font-medium">Toggle Theme</span> -->
          <label class="inline-flex items-center me-5 cursor-pointer">
            <input type="checkbox" value="" class="sr-only peer" :checked="!isDarkMode" @change="toggleDarkMode">
            <div class="relative w-11 h-6 bg-gray-200 rounded-full peer dark:bg-gray-700 peer-focus:ring-4 peer-focus:ring-purple-300 dark:peer-focus:ring-purple-800 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-purple-600 dark:peer-checked:bg-purple-600 after:z-10">
              <span class="absolute top-0.5 left-1 z-0 text-yellow-500">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" fill-rule="evenodd" clip-rule="evenodd"></path>
                </svg>
              </span>
              <span class="absolute top-0.5 right-1 z-0 text-gray-800 dark:text-gray-300">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
                </svg>
              </span>
            </div>
          </label>
        </div>

        <RouterLink
          to="/docs"
          class="hidden rounded-full border border-blue-200 bg-blue-50 px-4 py-2 text-sm font-semibold text-blue-700 transition hover:border-blue-300 hover:bg-blue-100 dark:border-blue-800 dark:bg-blue-950/40 dark:text-blue-300 dark:hover:bg-blue-950/70 md:inline-flex lg:hidden"
        >
          Docs
        </RouterLink>

        <button
          type="button"
          @click="toggleMenu"
          class="inline-flex h-10 w-10 items-center justify-center rounded-full border border-gray-200 bg-white text-gray-700 transition hover:border-gray-300 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200 dark:hover:border-gray-600 dark:hover:bg-gray-700 lg:hidden"
          :aria-expanded="mobileMenuOpen"
          aria-controls="mobile-menu"
          aria-label="Toggle navigation menu"
        >
          <svg v-if="isMenuOpen" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
    </div>

    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <div v-if="isMenuOpen" id="mobile-menu" class="border-t border-gray-200 bg-white px-4 py-3 dark:border-gray-700 dark:bg-gray-900 lg:hidden">
        <div class="mx-auto flex max-w-screen-xl flex-col gap-2">
          <button
            v-if="authLoaded && !isAuthenticated"
            type="button"
            @click="navigate('/auth/login')"
            class="rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 px-3 py-2 text-left text-sm font-semibold text-white transition hover:from-emerald-600 hover:to-teal-600"
          >
            Sign in
          </button>
          <button
            v-if="authLoaded && isAuthenticated"
            type="button"
            @click="navigate('/profile')"
            class="rounded-xl border border-emerald-300 bg-emerald-50 px-3 py-2 text-left text-sm font-semibold text-emerald-700 transition hover:bg-emerald-100 dark:border-emerald-500/40 dark:bg-emerald-500/10 dark:text-emerald-300 dark:hover:bg-emerald-500/20"
          >
            {{ authUser?.username || 'Profile' }}
          </button>
          <button
            v-if="authLoaded && isAuthenticated"
            type="button"
            @click="signOut"
            class="rounded-xl border border-rose-300 bg-rose-50 px-3 py-2 text-left text-sm font-semibold text-rose-700 transition hover:bg-rose-100 dark:border-rose-500/40 dark:bg-rose-500/10 dark:text-rose-300 dark:hover:bg-rose-500/20"
          >
            Sign out
          </button>
          <button
            v-for="item in navItems"
            v-show="!item.adminOnly || item.usable"
            :key="item.to"
            type="button"
            @click="navigate(item.to)"
            class="rounded-xl px-3 py-2 text-left text-sm font-medium transition-colors"
            :class="item.adminOnly ? 
              (route.path === item.to || route.path.startsWith('/admin') ? 'bg-purple-600 text-white dark:bg-purple-500' : 'text-gray-600 hover:bg-purple-50 hover:text-purple-700 dark:text-gray-300 dark:hover:bg-purple-900/30 dark:hover:text-purple-300') :
              (route.path === item.to || (item.to === '/docs' && route.path.startsWith('/docs')) ? 'bg-gray-900 text-white dark:bg-white dark:text-gray-900' : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-800 dark:hover:text-white')"
          >
            {{ item.label }}
          </button>
          <button
            type="button"
            @click="navigate('/docs')"
            class="mt-2 inline-flex items-center justify-center rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 px-4 py-3 text-sm font-semibold text-white shadow-lg transition hover:from-blue-700 hover:to-purple-700"
          >
            Open Documentation
          </button>
        </div>
      </div>
    </transition>
  </nav>
</template>
