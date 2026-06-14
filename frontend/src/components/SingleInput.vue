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
  <p v-if="props.requestVar" class="text-gray-100">Insert {{ props.defs.name }} <b>{{ props.requestVar }}</b></p>
  <form class="flex gap-4 flex-wrap" @submit.prevent="insertValue">
    <input v-model="inputValue" :type="props.defs.type" :name="props.defs.name" :placeholder="props.defs.placeholder" class="p-2 focus:outline-none dark:bg-gray-800 dark:text-gray-200 rounded-full" autocomplete="off" />
    <button class="bg-emerald-600 text-white px-6 py-2 rounded-full w-fit font-semibold">
      Insert
    </button>
    <button @click="props.defs.show = false" class="bg-red-600 text-white px-6 py-2 rounded-full w-fit font-semibold">
      Cancel
    </button>
  </form>
</template>
