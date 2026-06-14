<template>
  <!-- Overlay -->
  <Transition name="overlay" appear>
    <div
      v-if="visible"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-lg"
    >
      <!-- Dialog -->
      <Transition name="dialog" appear>
        <form @submit.prevent="close(true)"
          v-if="visible"
          class="w-full max-w-lg rounded-2xl bg-white/90 dark:bg-gray-900/90
                 border border-gray-200/70 dark:border-gray-700/70
                 shadow-xl backdrop-filter backdrop-blur-sm
                 p-8 space-y-6
                 transform-gpu transition-all duration-200
                 motion-reduce:transition-none"
        >
          <!-- Message -->
          <div class="text-center space-y-2">
            <p class="text-xl font-semibold text-gray-900 dark:text-gray-100">
              <span v-html="message"></span>
            </p>
          </div>
          <!-- Inputs (only for “input” type) -->
          <div v-if="type === 'input'" class="space-y-5">
            <div v-for="(el, i) in elements" :key="i" class="space-y-1">
              <label class="block text-sm font-medium text-gray-600 dark:text-gray-400">
                {{ el.label }}
              </label>
              <input v-if="el.type !== 'select'"
                v-model="inputs[el.name]"
                :type="el.type || 'text'"
                :placeholder="el.placeholder"
                :required="el.required || false"
                :autofocus="el.autofocus"
                class="w-full rounded-xl border border-gray-300 dark:border-gray-600
                       bg-white/70 dark:bg-gray-800/70 px-4 py-2
                       text-gray-900 dark:text-gray-100
                       focus:outline-none focus:ring-2 focus:ring-emerald-500
                       focus:border-transparent transition-colors"
              />
              <select v-else
                v-model="inputs[el.name]"
                :required="el.required || false"
                :autofocus="el.autofocus"
                :placeholder="el.placeholder || 'Select an option'"
                class="w-full rounded-xl border border-gray-300 dark:border-gray-600
                       bg-white/70 dark:bg-gray-800/70 px-4 py-2
                       text-gray-900 dark:text-gray-100
                       focus:outline-none focus:ring-2 focus:ring-emerald-500
                       focus:border-transparent transition-colors"
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
              class="px-5 py-2 rounded-xl text-sm font-medium
                     bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700
                     text-gray-800 dark:text-gray-200
                     transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-5 py-2 rounded-xl text-sm font-medium
                     bg-emerald-600 hover:bg-emerald-700 active:scale-95
                     text-white shadow-md
                     transition-transform"
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
