<template>
  <li class="flex items-center justify-between p-4 hover:bg-gray-100 dark:hover:text-white hover:text-gray-900 cursor-pointer dark:hover:bg-gray-800 rounded-full">
    <div class="flex gap-4">
      <slot name="icon"></slot>
      <slot name="descriptor"></slot>
    </div>
    <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
    </svg>
  </li>
</template>
