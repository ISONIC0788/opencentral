<template>
  <div class="min-h-screen bg-[#fafafa] dark:bg-[#000000] text-[#171717] dark:text-[#ffffff]">
    <main class="max-w-8xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Sidebar Navigation -->
        <div class="md:col-span-1">
          <div class="bg-[#ffffff] dark:bg-[#000000] border border-neutral-200/80 dark:border-neutral-800/80 rounded-md p-6 shadow-none">
            <h2 class="text-lg font-semibold mb-4 text-[#171717] dark:text-[#ffffff]">Admin Tools</h2>
            <nav class="space-y-2">
              <router-link
                to="/admin"
                exact
                class="block px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="$route.path === '/admin' ? 'bg-neutral-100 text-[#171717] dark:bg-neutral-900 dark:text-[#ffffff]' : 'text-neutral-500 hover:text-[#171717] hover:bg-neutral-50 dark:text-neutral-400 dark:hover:text-[#ffffff] dark:hover:bg-neutral-900/50'"
              >
                Overview
              </router-link>
            </nav>
            <div class="mt-6 pt-6 border-t border-neutral-200 dark:border-neutral-800">
              <p class="text-xs text-neutral-500 dark:text-neutral-400">
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
