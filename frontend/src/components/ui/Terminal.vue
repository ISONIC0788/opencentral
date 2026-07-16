<template>
  <div class="w-full bg-[#fafafa] dark:bg-[#0a0a0a] text-neutral-800 dark:text-[#fafafa] border border-neutral-200 dark:border-neutral-800 rounded-xl overflow-hidden font-mono shadow-2xl">
    <!-- Header/Chrome -->
    <div class="flex items-center px-4 py-3 border-b border-neutral-200 dark:border-neutral-900 bg-neutral-100/70 dark:bg-neutral-950/50">
      <div class="flex space-x-2">
        <span class="w-3 h-3 rounded-full bg-[#ff5f56]"></span>
        <span class="w-3 h-3 rounded-full bg-[#ffbd2e]"></span>
        <span class="w-3 h-3 rounded-full bg-[#27c93f]"></span>
      </div>
    </div>
    <!-- Content Area -->
    <div class="p-4 overflow-y-auto max-h-[600px] text-left leading-relaxed">
      <slot />
    </div>
  </div>
</template>

<script setup>
</script>
