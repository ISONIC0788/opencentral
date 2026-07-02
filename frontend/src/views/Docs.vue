<template>
  <div class="min-h-screen bg-[#fafafa] dark:bg-[#000000] text-[#171717] dark:text-[#ffffff]">
    <main class="max-w-8xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Sidebar Navigation -->
        <div class="md:col-span-1">
          <div class="bg-[#ffffff] dark:bg-[#000000] border border-neutral-200/80 dark:border-neutral-800/80 rounded-md p-6 shadow-none">
            <h2 class="text-lg font-semibold mb-4 text-[#171717] dark:text-[#ffffff]">Documentation</h2>
            <nav class="space-y-2">
              <router-link
                to="/docs"
                exact
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs' ? 'bg-neutral-100 text-[#171717] dark:bg-neutral-900 dark:text-[#ffffff]' : 'text-neutral-500 hover:text-[#171717] hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-[#ffffff] dark:hover:bg-neutral-900/50'"
              >
                Overview
              </router-link>
              <router-link
                to="/docs/viewing-logs"
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs/viewing-logs' ? 'bg-neutral-100 text-[#171717] dark:bg-neutral-900 dark:text-[#ffffff]' : 'text-neutral-500 hover:text-[#171717] hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-[#ffffff] dark:hover:bg-neutral-900/50'"
              >
                Viewing Logs
              </router-link>
              <router-link
                to="/docs/python"
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs/python' ? 'bg-neutral-100 text-[#171717] dark:bg-neutral-900 dark:text-[#ffffff]' : 'text-neutral-500 hover:text-[#171717] hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-[#ffffff] dark:hover:bg-neutral-900/50'"
              >
                Python SDK
              </router-link>
              <router-link
                to="/docs/javascript"
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs/javascript' ? 'bg-neutral-100 text-[#171717] dark:bg-neutral-900 dark:text-[#ffffff]' : 'text-neutral-500 hover:text-[#171717] hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-[#ffffff] dark:hover:bg-neutral-900/50'"
              >
                JavaScript SDK
              </router-link>
              <router-link
                to="/docs/go"
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs/go' ? 'bg-neutral-100 text-[#171717] dark:bg-neutral-900 dark:text-[#ffffff]' : 'text-neutral-500 hover:text-[#171717] hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-[#ffffff] dark:hover:bg-neutral-900/50'"
              >
                Go SDK
              </router-link>
              <router-link
                to="/docs/rust"
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs/rust' ? 'bg-neutral-100 text-[#171717] dark:bg-neutral-900 dark:text-[#ffffff]' : 'text-neutral-500 hover:text-[#171717] hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-[#ffffff] dark:hover:bg-neutral-900/50'"
              >
                Rust SDK
              </router-link>
              <router-link
                to="/docs/php"
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs/php' ? 'bg-neutral-100 text-[#171717] dark:bg-neutral-900 dark:text-[#ffffff]' : 'text-neutral-500 hover:text-[#171717] hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-[#ffffff] dark:hover:bg-neutral-900/50'"
              >
                PHP SDK
              </router-link>
            </nav>
          </div>
        </div>

        <!-- Main Content -->
        <div class="md:col-span-2">
          <router-view />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

onMounted(() => {
  // If we're on /docs, redirect to overview
  if (route.path === '/docs') {
    router.replace('/docs/overview')
  }
})
</script>
