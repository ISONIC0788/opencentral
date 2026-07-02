<!-- Toast api -->
<template>
  <div class="fixed bottom-5 right-5 z-50 flex flex-col gap-4">
    <div v-for="toast in toasts" :key="toast.id" class="flex flex-col animate-fade-in-up backdrop-blur-sm">
      <div 
        class="relative flex items-center max-w-4xl p-4 pr-6 rounded-md"
        :class="toast.type === 'success'
          ? 'bg-[#ffffff] dark:bg-[#0a0a0a] text-[#171717] dark:text-[#ffffff] border border-emerald-500/30'
          : toast.type === 'error'
          ? 'bg-[#ffffff] dark:bg-[#0a0a0a] border border-rose-500/30 text-rose-600 dark:text-rose-400'
          : toast.type === 'warning'
          ? 'bg-[#ffffff] dark:bg-[#0a0a0a] border border-amber-500/30 text-amber-600 dark:text-amber-400'
          : 'bg-[#ffffff] dark:bg-[#0a0a0a] border border-neutral-200 dark:border-neutral-800 text-[#171717] dark:text-[#ffffff]'"
        >
        <!-- Icon -->
        <div class="flex-shrink-0 mr-3">
          <svg v-if="toast.type === 'success'" class="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else-if="toast.type === 'error'" class="w-6 h-6 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <svg v-else-if="toast.type === 'warning'" class="w-6 h-6 text-amber-500" stroke="currentColor" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path opacity="0.5" d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" fill="currentColor"/>
            <path d="M12 17.75C12.4142 17.75 12.75 17.4142 12.75 17V11C12.75 10.5858 12.4142 10.25 12 10.25C11.5858 10.25 11.25 10.5858 11.25 11V17C11.25 17.4142 11.5858 17.75 12 17.75Z" fill="currentColor"/>
            <path d="M12 7C12.5523 7 13 7.44771 13 8C13 8.55229 12.5523 9 12 9C11.4477 9 11 8.55229 11 8C11 7.44771 11.4477 7 12 7Z" fill="currentColor"/>
          </svg>
          <svg v-else class="w-6 h-6 text-neutral-500 dark:text-neutral-400" stroke="currentColor" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path opacity="0.5" d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" fill="currentColor"/>
            <path d="M12 17.75C12.4142 17.75 12.75 17.4142 12.75 17V11C12.75 10.5858 12.4142 10.25 12 10.25C11.5858 10.25 11.25 10.5858 11.25 11V17C11.25 17.4142 11.5858 17.75 12 17.75Z" fill="currentColor"/>
            <path d="M12 7C12.5523 7 13 7.44771 13 8C13 8.55229 12.5523 9 12 9C11.4477 9 11 8.55229 11 8C11 7.44771 11.4477 7 12 7Z" fill="currentColor"/>
          </svg>
        </div>

        <!-- Message -->
        <div class="flex-grow">
          <span class="font-medium text-sm" v-html="toast.message"></span>
        </div>
      </div>

      <div class="ml-auto space-x-2 flex mt-1">
        <!-- Subtle timer bar -->
        <div
          v-if="toast.duration"
          class="hover:hidden px-2 bg-neutral-100 text-neutral-600 dark:bg-neutral-900 dark:text-neutral-400 rounded-md text-xs font-mono flex items-center"
        >
          {{ toast.duration / 1000 }}
        </div>
        <button
          @click="removeToast(toast.id)"
          class="p-1 focus:outline-none rounded-md hover:bg-neutral-100 dark:hover:bg-neutral-900 transition-colors"
          :class="toast.type === 'error' ? 'text-rose-600 dark:text-rose-400' : toast.type === 'warning' ? 'text-amber-600 dark:text-amber-400' : 'text-[#171717] dark:text-[#ffffff]'"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

let toastId = 1;
export const toasts = ref([]);

export function addToast(message, config = {}) {
  const { type = 'info', duration = null } = config;
  const id = toastId++;
  toasts.value.push({ id, message, type, duration });
  const index = toasts.value.findIndex((t) => t.id === id);
  if (duration && duration > 0) {
    const interval = setInterval(() => {
      try {
        toasts.value[index].duration -= 1000;
        if (toasts.value[index].duration <= 0) {
          removeToast(id);
          clearInterval(interval);
        }
      } catch (e) {
        removeToast(id);
        clearInterval(interval);
      }
    }, 1000);
  }
  return id;
}

export function removeToast(id) {
  const index = toasts.value.findIndex((toast) => toast.id === id);
  if (index !== -1) toasts.value.splice(index, 1);
}

export default {
  name: 'Toast',
  setup() {
    return { toasts, removeToast };
  },
};
</script>

<style scoped>
/* Toast transition (fade-slide effect) */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}
.toast-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.95);
}
.toast-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
}

/* Slight bounce animation on entry */
@keyframes fade-in-up {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
.animate-fade-in-up {
  animation: fade-in-up 0.4s ease-out;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(0, 0, 0, 0.05);
}
:global(.dark) .animate-fade-in-up {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1);
}
</style>
