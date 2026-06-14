<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white">
    <main class="max-w-8xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Sidebar Navigation -->
        <div class="md:col-span-1">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
            <h2 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Admin Tools</h2>
            <nav class="space-y-2">
              <router-link
                to="/admin"
                exact
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/admin' ? 'bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300' : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'"
              >
                Overview
              </router-link>
            </nav>
            <div class="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
              <p class="text-xs text-gray-500 dark:text-gray-400">
                Admin access required for these tools.
              </p>
            </div>
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
</script>
