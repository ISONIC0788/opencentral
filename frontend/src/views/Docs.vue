<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white">
    <main class="max-w-8xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Sidebar Navigation -->
        <div class="md:col-span-1">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
            <h2 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Documentation</h2>
            <nav class="space-y-2">
              <router-link
                to="/docs"
                exact
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs' ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'"
              >
                Overview
              </router-link>
              <router-link
                to="/docs/viewing-logs"
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs/viewing-logs' ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'"
              >
                Viewing Logs
              </router-link>
              <router-link
                to="/docs/python"
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs/python' ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'"
              >
                Python SDK
              </router-link>
              <router-link
                to="/docs/javascript"
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs/javascript' ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'"
              >
                JavaScript SDK
              </router-link>
              <router-link
                to="/docs/go"
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs/go' ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'"
              >
                Go SDK
              </router-link>
              <router-link
                to="/docs/rust"
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs/rust' ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'"
              >
                Rust SDK
              </router-link>
              <router-link
                to="/docs/php"
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/docs/php' ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'"
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
