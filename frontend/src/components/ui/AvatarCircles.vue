<template>
  <div class="z-10 flex -space-x-4 rtl:space-x-reverse">
    <a
      v-for="(url, index) in avatarUrls"
      :key="index"
      :href="url.profileUrl"
      target="_blank"
      rel="noopener noreferrer"
    >
      <img
        class="h-10 w-10 rounded-full border-2 border-white dark:border-neutral-800"
        :src="url.imageUrl"
        width="40"
        height="40"
        :alt="`Avatar ${index + 1}`"
      />
    </a>
    <a
      v-if="numPeople > 0"
      class="flex h-10 w-10 items-center justify-center rounded-full border-2 border-white bg-black text-center text-xs font-medium text-white hover:bg-neutral-800 dark:border-neutral-800 dark:bg-white dark:text-black dark:hover:bg-neutral-200 transition-colors"
      href=""
      @click.prevent
    >
      +{{ numPeople }}
    </a>
  </div>
</template>

<script setup>
defineProps({
  numPeople: {
    type: Number,
    default: 0
  },
  avatarUrls: {
    type: Array,
    default: () => []
  }
})
</script>
