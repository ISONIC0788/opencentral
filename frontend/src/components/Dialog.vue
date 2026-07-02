<template>
  <!-- Overlay -->
  <Transition name="overlay" appear>
    <div
      v-if="visible"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/20 backdrop-blur-md"
    >
      <!-- Dialog -->
      <Transition name="dialog" appear>
        <form @submit.prevent="close(true)"
          v-if="visible"
          class="w-full max-w-lg rounded-md bg-[#ffffff] dark:bg-[#000000] border border-neutral-200 dark:border-neutral-800 shadow-xl p-8 space-y-6 transform-gpu transition-all duration-200 motion-reduce:transition-none"
        >
          <!-- Message -->
          <div class="text-center space-y-2">
            <p class="text-xl font-semibold text-[#171717] dark:text-[#ffffff]">
              <span v-html="message"></span>
            </p>
          </div>
          <!-- Inputs (only for “input” type) -->
          <div v-if="type === 'input'" class="space-y-5">
            <div v-for="(el, i) in elements" :key="i" class="space-y-1">
              <label class="block text-sm font-medium text-neutral-500 dark:text-neutral-400">
                {{ el.label }}
              </label>
              <input v-if="el.type !== 'select'"
                v-model="inputs[el.name]"
                :type="el.type || 'text'"
                :placeholder="el.placeholder"
                :required="el.required || false"
                :autofocus="el.autofocus"
                class="w-full rounded-md border border-neutral-200 dark:border-neutral-700 bg-[#ffffff] dark:bg-[#000000] px-4 py-2 text-[#171717] dark:text-[#ffffff] focus:outline-none focus:ring-1 focus:ring-neutral-400 focus:border-transparent transition-colors text-sm"
              />
              <select v-else
                v-model="inputs[el.name]"
                :required="el.required || false"
                :autofocus="el.autofocus"
                :placeholder="el.placeholder || 'Select an option'"
                class="w-full rounded-md border border-neutral-200 dark:border-neutral-700 bg-[#ffffff] dark:bg-[#000000] px-4 py-2 text-[#171717] dark:text-[#ffffff] focus:outline-none focus:ring-1 focus:ring-neutral-400 focus:border-transparent transition-colors text-sm"
              >
                <option v-for="option in el.options" :key="option" :value="option">
                  {{ option }}
                </option>
              </select>
            </div>
          </div>
          <!-- Actions -->
          <div class="flex justify-end gap-4 pt-2">
            <button
              v-if="type !== 'alert'"
              type="button"
              @click="close(false)"
              class="px-5 py-2 rounded-md text-sm font-medium bg-neutral-100 hover:bg-neutral-200 dark:bg-neutral-900 dark:hover:bg-neutral-800/80 text-[#171717] dark:text-[#ffffff] transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-5 py-2 rounded-md text-sm font-medium bg-[#171717] text-[#ffffff] dark:bg-[#ffffff] dark:text-[#000000] hover:bg-neutral-800 dark:hover:bg-neutral-100 shadow-sm transition-colors"
            >
              {{ type === 'input' ? 'Continue' : 'OK' }}
            </button>
          </div>
        </form>
      </Transition>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  type: String,
  message: String,
  elements: Array
});

const emit = defineEmits(['resolve']);

const visible = ref(true);
const inputs = ref({});

const close = (confirmed) => {
  visible.value = false;
  emit('resolve', {
    confirmed,
    data: inputs.value
  });
};

// ESC to close
const handler = (e) => {
  if (e.key === 'Escape') close(false);
};

onMounted(() => {
  window.addEventListener('keydown', handler);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handler);
});
</script>

<style>
/* Overlay fade */
.overlay-enter-active,
.overlay-leave-active {
  transition: opacity 0.2s ease;
}
.overlay-enter-from,
.overlay-leave-to {
  opacity: 0;
}

/* Dialog pop */
.dialog-enter-active {
  transition: all 0.2s ease;
}
.dialog-leave-active {
  transition: all 0.15s ease;
}

.dialog-enter-from {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}

.dialog-leave-to {
  opacity: 0;
  transform: scale(0.97) translateY(5px);
}
</style>
