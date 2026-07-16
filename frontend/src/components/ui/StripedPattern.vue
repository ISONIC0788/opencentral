<template>
  <svg
    aria-hidden="true"
    class="pointer-events-none absolute inset-0 z-0 h-full w-full stroke-[0.5] stroke-neutral-900/[0.07] dark:stroke-white/[0.04]"
    xmlns="http://www.w3.org/2000/svg"
  >
    <defs>
      <pattern
        :id="id"
        :width="w"
        :height="h"
        patternUnits="userSpaceOnUse"
        :x="x"
        :y="y"
      >
        <template v-if="direction === 'left'">
          <line x1="0" :y1="h" :x2="w" y2="0" stroke="currentColor" />
          <line :x1="-w" :y1="h" x2="0" y2="0" stroke="currentColor" />
          <line :x1="w" :y1="h" :x2="w * 2" y2="0" stroke="currentColor" />
        </template>
        <template v-else>
          <line x1="0" y1="0" :x2="w" :y2="h" stroke="currentColor" />
          <line :x1="-w" y1="0" x2="0" :y2="h" stroke="currentColor" />
          <line :x1="w" y1="0" :x2="w * 2" :y2="h" stroke="currentColor" />
        </template>
      </pattern>
    </defs>
    <rect width="100%" height="100%" :fill="`url(#${id})`" />
  </svg>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  width: {
    type: [Number, String],
    default: 40
  },
  height: {
    type: [Number, String],
    default: 40
  },
  x: {
    type: [Number, String],
    default: -1
  },
  y: {
    type: [Number, String],
    default: -1
  },
  direction: {
    type: String,
    default: 'left',
    validator: (val) => ['left', 'right'].includes(val)
  }
})

const id = 'striped-pattern-' + Math.random().toString(36).substring(2, 9)

const w = computed(() => Number(props.width))
const h = computed(() => Number(props.height))
</script>
