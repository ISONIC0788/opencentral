<script setup>
import { computed } from 'vue'
import AppButton from './AppButton.vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Log Machine Central'
  }
})

// Split words for text presentation stagger effect
const words = computed(() => props.title.split(' '))

// Dynamic generation of paths matching your configuration path coordinates
const generatePaths = (position) => {
  return Array.from({ length: 36 }, (_, i) => ({
    id: i,
    d: `M-${380 - i * 5 * position} -${189 + i * 6}C-${
        380 - i * 5 * position
    } -${189 + i * 6} -${312 - i * 5 * position} ${216 - i * 6} ${
        152 - i * 5 * position
    } ${343 - i * 6}C${616 - i * 5 * position} ${470 - i * 6} ${
        684 - i * 5 * position
    } ${875 - i * 6} ${684 - i * 5 * position} ${875 - i * 6}`,
    width: 0.5 + i * 0.03,
    // Add random delay variances per path element like Math.random() in the React original
    delay: `${(i * 0.2).toFixed(1)}s`
  }))
}

const positivePaths = generatePaths(1)
const negativePaths = generatePaths(-1)
</script>

<template>
  <div class="relative min-h-screen w-full flex items-center justify-center overflow-hidden bg-white dark:bg-neutral-950">
    
    <div class="absolute inset-0 pointer-events-none">
      <svg class="w-full h-full text-neutral-950/20 dark:text-white/10" viewBox="0 0 696 316" fill="none">
        <title>Background Paths</title>
        
        <path
          v-for="path in positivePaths"
          :key="'pos-' + path.id"
          :d="path.d"
          stroke="currentColor"
          :stroke-width="path.width"
          stroke-dasharray="500"
          class="animate-path-slow"
          :style="{ animationDelay: path.delay }"
        />

        <path
          v-for="path in negativePaths"
          :key="'neg-' + path.id"
          :d="path.d"
          stroke="currentColor"
          :stroke-width="path.width"
          stroke-dasharray="500"
          class="animate-path-slow"
          :style="{ animationDelay: path.delay }"
        />
      </svg>
    </div>

    <div class="relative z-10 container mx-auto px-4 md:px-6 text-center">
      <div class="max-w-4xl mx-auto transition-opacity duration-1000 ease-out">
        
        <h1 class="text-5xl sm:text-7xl md:text-8xl font-bold mb-8 tracking-tighter text-neutral-900 dark:text-white">
          <span v-for="(word, wIdx) in words" :key="wIdx" class="inline-block mr-4 last:mr-0">
            <span 
              v-for="(letter, lIdx) in word.split('')" 
              :key="lIdx"
              class="inline-block translate-y-0 opacity-100 transition-all duration-700 bg-clip-text text-transparent bg-gradient-to-r from-neutral-900 to-neutral-700/80 dark:from-white dark:to-white/80"
              :style="{ transitionDelay: `${(wIdx * 0.1 + lIdx * 0.03).toFixed(2)}s` }"
            >
              {{ letter }}
            </span>
          </span>
        </h1>

        <div class="inline-block group relative bg-gradient-to-b from-black/10 to-white/10 dark:from-white/10 dark:to-black/10 p-px rounded-2xl backdrop-blur-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300">
          <AppButton
            variant="ghost"
            class="rounded-[1.15rem] px-8 py-6 text-lg font-semibold backdrop-blur-md bg-white/95 hover:bg-white/100 dark:bg-black/95 dark:hover:bg-black/100 text-black dark:text-white transition-all duration-300 group-hover:-translate-y-0.5 border border-black/10 dark:border-white/10 hover:shadow-md dark:hover:shadow-neutral-800/50"
          >
            <span class="opacity-90 group-hover:opacity-100 transition-opacity">
              Discover Excellence
            </span>
            <span class="ml-3 opacity-70 group-hover:opacity-100 group-hover:translate-x-1.5 transition-all duration-300">
              →
            </span>
          </AppButton>
        </div>

      </div>
    </div>
  </div>
</template>