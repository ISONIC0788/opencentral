<!-- Toast api -->
<template>
  <div class="fixed bottom-5 right-5 z-50 flex flex-col gap-4">
    <div v-for="toast in toasts" :key="toast.id" class="flex flex-col animate-fade-in-up shadow-2xl backdrop-blur-sm text-white">
      <div 
        class="relative flex items-center max-w-4xl p-4 pr-6 rounded-xl"
        :class="toast.type === 'success'
          ? 'bg-gradient-to-r from-emerald-500 to-green-600'
          : toast.type === 'error'
          ? 'bg-gradient-to-r from-rose-500 to-red-600'
          : toast.type === 'warning'
          ? 'bg-amber-600 dark:bg-amber-600'
          : 'bg-gradient-to-r from-sky-500 to-blue-600'"
        >
        <!-- Icon -->
        <div class="flex-shrink-0 mr-3">
          <svg v-if="toast.type === 'success'" class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else-if="toast.type === 'error'" class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <svg v-else-if="toast.type === 'warning'" class="w-6 h-6" stroke="currentColor" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path opacity="0.5" d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" fill="#1C274C"/>
            <path d="M12 17.75C12.4142 17.75 12.75 17.4142 12.75 17V11C12.75 10.5858 12.4142 10.25 12 10.25C11.5858 10.25 11.25 10.5858 11.25 11V17C11.25 17.4142 11.5858 17.75 12 17.75Z" fill="#1C274C"/>
            <path d="M12 7C12.5523 7 13 7.44771 13 8C13 8.55229 12.5523 9 12 9C11.4477 9 11 8.55229 11 8C11 7.44771 11.4477 7 12 7Z" fill="#1C274C"/>
          </svg>
          <svg v-else class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" >
            <path opacity="0.5" d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" fill="#1C274C"/>
            <path d="M12 17.75C12.4142 17.75 12.75 17.4142 12.75 17V11C12.75 10.5858 12.4142 10.25 12 10.25C11.5858 10.25 11.25 10.5858 11.25 11V17C11.25 17.4142 11.5858 17.75 12 17.75Z" fill="#1C274C"/>
            <path d="M12 7C12.5523 7 13 7.44771 13 8C13 8.55229 12.5523 9 12 9C11.4477 9 11 8.55229 11 8C11 7.44771 11.4477 7 12 7Z" fill="#1C274C"/>
          </svg>
        </div>

        <!-- Message -->
        <div class="flex-grow">
          <span class="font-medium" v-html="toast.message"></span>
        </div>
      </div>

      <div class="ml-auto space-x-2 flex"
      >
        <!-- Subtle timer bar -->
        <div
          v-if="toast.duration"
          class="hover:hidden rounded-full px-2"
          :class="toast.type === 'success'
            ? 'bg-gradient-to-r from-emerald-500 to-green-600'
            : toast.type === 'error'
            ? 'bg-gradient-to-r from-rose-500 to-red-600'
            : toast.type === 'warning'
            ? 'bg-amber-600 dark:bg-amber-600'
            : 'bg-gradient-to-r from-sky-500 to-blue-600'"
        >
          {{ toast.duration / 1000 }}
        </div>
        <button
          @click="removeToast(toast.id)"
          class="p-1 focus:outline-none rounded-full bg-red-500 hover:bg-white/20 transition-colors"
        >
          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" >
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
}

/* Timer progress bar animation */
@keyframes toast-progress {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}
.animate-toast-progress {
  animation: toast-progress linear forwards;
  animation-duration: 1s;
}

/* Optional glow for success/error vibes */
.bg-green-500,
.bg-gradient-to-r.from-emerald-500 {
  box-shadow: 0 0 15px rgba(16, 185, 129, 0.5);
}
.bg-red-500,
.bg-gradient-to-r.from-rose-500 {
  box-shadow: 0 0 15px rgba(239, 68, 68, 0.5);
}
.bg-yellow-500,
.bg-gradient-to-r.from-amber-400 {
  box-shadow: 0 0 15px rgba(234, 179, 8, 0.5);
}
.bg-blue-500,
.bg-gradient-to-r.from-sky-500 {
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
}
</style>
