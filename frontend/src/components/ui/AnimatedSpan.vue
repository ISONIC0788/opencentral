<template>
  <span
    class="animated-span block opacity-0"
    :style="{ animationDelay: `${delay}ms` }"
  >
    <slot />
  </span>
</template>

<script setup>
defineProps({
  delay: {
    type: Number,
    default: 0
  }
})
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animated-span {
  animation: fadeIn 300ms forwards ease-out;
}
</style>
