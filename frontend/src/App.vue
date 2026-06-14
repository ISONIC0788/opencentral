<script setup>
  import { computed, onMounted } from 'vue'
  import { RouterView, useRoute } from 'vue-router';
  import HeaderView from './views/HeaderView.vue';
  import Loading from './components/Loading.vue';
  import { isLoading } from './components/isLoading';
  import { auth } from '@/stores/auth';
  import Toast from './components/Toast.vue';

  const route = useRoute()
  const showChrome = computed(() => !route.path.startsWith('/auth'))

  onMounted(() => {
    isLoading.value = true
    auth.bootstrapSession()
      .catch((err) => {
        console.error('Error bootstrapping session:', err)
      })
      .finally(() => {
        isLoading.value = false
      })
  })
</script>

<template>
  <header v-if="auth.state.loaded && showChrome" class="fixed w-full top-0 z-20">
    <HeaderView />
  </header>

  <RouterView v-if="auth.state.loaded" :style="showChrome ? 'margin-top: 70px;' : ''" />

  <Loading v-if="isLoading">
    <template #dialog>
      Loading, please wait...
    </template>
  </Loading>
  <ChatBot v-if="showChrome" :title="`Log Machine Analyst`" :description="`The analyst is ready to help you debug. <br> Ask anything about the logs!`" />
  <Toast />
</template>
