<template>
  <span class="typing-animation block">
    {{ displayedText }}<span v-if="showCursor" class="cursor">|</span>
  </span>
</template>

<script setup>
import { ref, onMounted, onUnmounted, useSlots } from 'vue'

const props = defineProps({
  text: {
    type: String,
    default: ''
  },
  delay: {
    type: Number,
    default: 0
  },
  duration: {
    type: Number,
    default: 60
  }
})

const slots = useSlots()
const displayedText = ref('')
const showCursor = ref(true)
let typingInterval = null
let delayTimeout = null

const getRawText = () => {
  if (props.text) return props.text
  if (slots.default) {
    const children = slots.default()
    return children.reduce((acc, child) => {
      if (typeof child.children === 'string') {
        return acc + child.children
      }
      return acc
    }, '')
  }
  return ''
}

onMounted(() => {
  const fullText = getRawText()
  delayTimeout = setTimeout(() => {
    let index = 0
    typingInterval = setInterval(() => {
      if (index < fullText.length) {
        displayedText.value += fullText.charAt(index)
        index++
      } else {
        clearInterval(typingInterval)
        showCursor.value = false
      }
    }, props.duration)
  }, props.delay)
})

onUnmounted(() => {
  if (delayTimeout) clearTimeout(delayTimeout)
  if (typingInterval) clearInterval(typingInterval)
})
</script>

<style scoped>
.cursor {
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  from, to { color: transparent }
  50% { color: currentColor }
}
</style>
