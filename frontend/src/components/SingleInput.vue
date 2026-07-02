<script setup>
  import { ref } from 'vue';
  const props = defineProps({
    defs: {
      type: Object,
      required: true
    },
    requestVar: {
      type: String,
      required: false
    }
  });

  const inputValue = ref('');

  function insertValue() {
    if (props.defs.varType === Object || props.defs.varType === Array) {
      props.defs.value[props.requestVar] = inputValue.value;
    } else {
      props.defs.value = inputValue.value;
    }
    props.defs.show = false;
  }
</script>
<template>
  <p v-if="props.requestVar" class="text-[#171717] dark:text-[#ffffff] text-sm font-medium">Insert {{ props.defs.name }} <b>{{ props.requestVar }}</b></p>
  <form class="flex gap-3 flex-wrap" @submit.prevent="insertValue">
    <input v-model="inputValue" :type="props.defs.type" :name="props.defs.name" :placeholder="props.defs.placeholder" class="px-3 py-2 text-sm bg-[#ffffff] dark:bg-[#000000] border border-neutral-200 dark:border-neutral-700 rounded-md text-[#171717] dark:text-[#ffffff] focus:outline-none focus:ring-1 focus:ring-neutral-400 outline-none transition-colors" autocomplete="off" />
    <button class="px-4 py-2 bg-[#171717] text-[#ffffff] dark:bg-[#ffffff] dark:text-[#000000] hover:bg-neutral-800 dark:hover:bg-neutral-100 font-semibold text-sm rounded-md transition-colors w-fit">
      Insert
    </button>
    <button type="button" @click="props.defs.show = false" class="px-4 py-2 border border-neutral-200 dark:border-neutral-800 bg-transparent text-[#171717] dark:text-[#ffffff] hover:bg-neutral-50 dark:hover:bg-neutral-900 font-semibold text-sm rounded-md transition-colors w-fit">
      Cancel
    </button>
  </form>
</template>
