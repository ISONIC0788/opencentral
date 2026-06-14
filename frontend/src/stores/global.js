import { reactive } from 'vue';

export const globals = reactive({
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  baseUrl: import.meta.env.VITE_BASE_URL || '/',
});
