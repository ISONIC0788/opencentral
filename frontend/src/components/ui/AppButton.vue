<script setup>
defineProps({
  variant: {
    type: String,
    default: 'default'
  }
})
</script>

<template>
  <button
    :class="[
      'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
      variant === 'ghost' ? 'hover:bg-neutral-100 dark:hover:bg-neutral-800 text-neutral-900 dark:text-white' : 'bg-neutral-900 text-white dark:bg-white dark:text-neutral-900'
    ]"
  >
    <slot />
  </button>
</template>