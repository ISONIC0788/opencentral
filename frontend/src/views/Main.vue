<script setup>
import { ref, reactive, computed, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import router from '@/router'
import { io } from 'socket.io-client'
import { globals } from '@/stores/global'
import { apiDelete, apiGet, apiPost, apiPut } from '@/stores/api'
import { auth } from '@/stores/auth'
import { useDialog } from '@/components/useDialog'
import { addToast } from '@/components/Toast.vue'

const apiUrl = new URL(globals.apiUrl)
const route = useRoute()
const dialog = useDialog()

const sidebarVisible = ref(true)
const selectedUser = ref(null)
const roomInfo = ref(null)
const shareUsername = ref('')
const shareCanWrite = ref(false)
const showSettings = ref(false)
const viewers = ref([])
const roomUsage = ref(null)
const usageLoading = ref(false)
const usageError = ref('')
const filter = ref({
  module: '',
  timestamp: '',
  message: ''
})

const socket = io(apiUrl.origin, {
  path: apiUrl.pathname.replace(/\/+$/, '') + '/socket.io',
  transports: ['websocket', 'polling'],
  withCredentials: true,
})

const users = reactive({})

const logGroupStyles = {
  SUCCESS: 'bg-emerald-600',
  INFO: 'bg-blue-600',
  WARNING: 'bg-amber-600',
  ERROR: 'bg-red-600',
  DEBUG: 'bg-purple-600',
  DEFAULT: 'bg-gray-600'
}

// Computed filtered logs for current user
const filteredLogs = computed(() => {
  if (!selectedUser.value || !users[selectedUser.value]) return []
  
  const userLogs = users[selectedUser.value].logs
  const tsFilter = filter.value.timestamp ? new Date(filter.value.timestamp) : new Date(0)

  return userLogs.filter(log => {
    return (
      (!filter.value.module || log.module?.toLowerCase().includes(filter.value.module.toLowerCase())) &&
      (!filter.value.message || log.message?.toLowerCase().includes(filter.value.message.toLowerCase())) &&
      log.timestamp >= tsFilter
    )
  })
})

const usagePercent = computed(() => {
  const value = Number(roomUsage.value?.usage_percent ?? 0)
  if (!Number.isFinite(value)) return 0
  return Math.max(0, Math.min(100, value))
})

function getActiveLevels() {
  if (!selectedUser.value || !users[selectedUser.value]) return []
  const levels = new Set()
  filteredLogs.value.forEach(log => levels.add(log.level))
  return Array.from(levels).sort()
}

function getLogsByLevel(level) {
  return filteredLogs.value.filter(log => log.level === level)
}

function formatTimestamp(date) {
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true
  })
}

async function joinRoom(roomId = null) {
  if (!roomId) {
    const { confirmed, data } = await dialog.input('Enter room ID to join:', [
      { label: "Room Name", type: "text", name: "room", id: "room_id", class: "rounded-full p-2 outline-none", placeholder: "Room ID", required: true, autofocus: true }
    ]);

    if (!confirmed || !data.room.trim()) return
    roomId = data.room.trim()
  }
  router.push({ query: { room: roomId } })
  return roomId
}

async function loadRoom(useCache = true) {
  if (!useCache && route.query.room) {
    socket.emit('leave', { room: route.query.room })
    Object.keys(users).forEach(key => delete users[key])
    selectedUser.value = null
    roomInfo.value = null
  }

  let cachedRoom = useCache ? route.query.room || localStorage.getItem('lastRoom') : null
  if (useCache && !cachedRoom && auth.state.user)
    cachedRoom = auth.state.user.username // Auto-join personal room if no room in query or cache

  const normalizedRoom = await joinRoom(cachedRoom);
  if (!normalizedRoom) {
    roomInfo.value = null
    roomUsage.value = null
    return
  }

  try {
    roomInfo.value = await apiGet(`/rooms/${encodeURIComponent(normalizedRoom)}`)
    // Reset users when receiving full history
    Object.keys(users).forEach(key => delete users[key])
    socket.emit('join', { room: normalizedRoom })
    localStorage.setItem('lastRoom', normalizedRoom)
    socket.emit('get_logs', { room: normalizedRoom }, (response) => {
      if (response?.status === 'error') {
        addToast(response.message, { type: 'error', duration: 5000 })
      }
    })
  } catch (error) {
    roomInfo.value = null
    roomUsage.value = null
    if (error.message.includes('Room not found')) {
      const { confirmed } = await dialog.confirm('The room you are trying to access does not exist. Do you want to create it?')
      router.push(confirmed ? { name: 'profile', query: { action: 'create', key: 'room', value: normalizedRoom } } : { query: {} })
    } else {
      addToast(error.message || 'Could not load room details', { type: 'error', duration: 5000 })
    }
  }
}

function formatBytes(bytes) {
  const value = Number(bytes || 0)
  if (!Number.isFinite(value) || value <= 0) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  const idx = Math.min(Math.floor(Math.log(value) / Math.log(1024)), units.length - 1)
  const scaled = value / Math.pow(1024, idx)
  return `${scaled >= 10 ? scaled.toFixed(0) : scaled.toFixed(1)} ${units[idx]}`
}


function openSettings() {
  showSettings.value = true
}

async function updateVisibility(visibility) {
  if (!route.query.room) {
    return
  }
  try {
    const payload = await apiPut(`/rooms/${encodeURIComponent(route.query.room)}/visibility`, { visibility })
    roomInfo.value = payload.room || roomInfo.value
  } catch (error) {
    addToast(error.message || 'Could not update visibility', { type: 'error', duration: 5000 })
  }
}

async function shareRoom() {
  if (!route.query.room || !shareUsername.value.trim()) {
    return
  }
  try {
    const payload = await apiPost(`/rooms/${encodeURIComponent(route.query.room)}/share`, {
      username: shareUsername.value.trim(),
      can_write: shareCanWrite.value,
    })
    roomInfo.value = payload.room || roomInfo.value
    shareUsername.value = ''
    shareCanWrite.value = false
  } catch (error) {
    addToast(error.message || 'Could not share room', { type: 'error', duration: 5000 })
  }
}

async function unshareRoom(username) {
  if (!route.query.room || !username) {
    return
  }
  try {
    const payload = await apiDelete(`/rooms/${encodeURIComponent(route.query.room)}/share/${encodeURIComponent(username)}`)
    roomInfo.value = payload.room || roomInfo.value
  } catch (error) {
    addToast(error.message || 'Could not unshare room', { type: 'error', duration: 5000 })
  }
}

function selectUser(userName) {
  selectedUser.value = userName
}

function handleIncomingLog(log) {
  const username = log.username || log.user || 'unknown';
  if (!users[username]) {
    users[username] = {
      name: username,
      avatar: log.avatar_url,
      logs: [],
      logGroups: new Set()
    }
  }

  log.timestamp = new Date(log.timestamp)
  users[username].logs.unshift(log)        // newest first
  users[username].logGroups.add(log.level)

  // Auto-select first user
  if (!selectedUser.value) {
    selectedUser.value = username
  }
}

async function sendATestLog() {
  /* if (!route.query.room) {
    addToast('Please join a room first to send a test log', { type: 'warning', duration: 5000 })
    return
  } */

  const { confirmed, data } = await dialog.input('Send a test log', [
    { type: 'select', options: ['SUCCESS', 'INFO', 'WARNING', 'ERROR', 'DEBUG'], label: 'Log Level', name: 'level', id: 'log_level', class: 'rounded-full p-2 outline-none', required: true, autofocus: true },
    { label: "Message", type: "text", name: "message", id: "log_message", class: "rounded-full p-2 outline-none", placeholder: "Log message", required: true, autofocus: true }
  ])

  if (!confirmed) return;
  const { level, message } = data;

  console.log('Sending test log:', { level, message })

  socket.emit('log', {
    room: route.query.room,
    data: {
      user: auth.state.user?.username || 'test_user',
      level, message,
      module: 'TestModule',
      timestamp: new Date().toISOString()
    }
  }, (response) => {
    if (response?.status !== 'queued') {
      addToast(response?.message || 'Failed to send test log', { type: 'error', duration: 5000 })
    } else {
      handleIncomingLog({
        user: auth.state.user?.username || 'test_user',
        level, message,
        module: 'TestModule',
        timestamp: new Date()
      })
      addToast('Test log sent successfully', { type: 'success', duration: 3000 })
    }
  })
}

function clearLogs() {
  const username = auth.state.user?.username
  if (!selectedUser.value || !users[selectedUser.value] || !users[username]) return

  dialog.confirm(`Are you sure you want to clear all logs for ${username}? This action cannot be undone.`).then(({ confirmed }) => {
    if (!confirmed) return
    socket.emit('clear_logs', route.query.room, (response) => {
      if (response?.status !== 'success') {
        addToast(response?.message || 'Failed to clear logs', { type: 'error', duration: 5000 })
      } else {
        users[username].logs = []
        users[username].logGroups.clear()
        addToast(`Your logs have been cleared successfully`, { type: 'success', duration: 3000 })
      }
    })
  })
}

function copyToClipboard(text, event) {
  const button = event.currentTarget
  button.textContent = '✅ Copied'
  button.classList.add('bg-green-100', 'text-green-800')
  navigator.clipboard.writeText(text)
  setTimeout(() => {
    button.classList.remove('bg-green-100', 'text-green-800')
    button.textContent = '📋 Copy'
  }, 3000);
}

// Socket Setup
socket.on('connect', () => {
  loadRoom()
  onBeforeUnmount(() => {
    socket.disconnect()
  });
})

socket.on('logs', (data) => {
  // console.log(data);
  data.logs.forEach(log => handleIncomingLog(log))
})

socket.on('log', handleIncomingLog)
socket.on('room:presence', (payload) => {
  viewers.value = payload?.viewers || []
})

socket.on('error', (errorText) => {
  addToast(errorText || 'Room operation failed', { type: 'error', duration: 5000 })
  if (errorText.includes('not found')) {
    dialog.confirm('The room you are trying to access does not exist. Do you want to create it?').then(({ confirmed }) => {
      if (confirmed) {
        router.push({ name: 'profile', query: { action: 'create', key: 'room', value: route.query.room } })
      }
    })
  }
})

socket.on('logs_cleared', (data) => {
  const { room, username } = data
  if (users[username] && room === route.query.room) {
    users[username].logs = []
    users[username].logGroups.clear()
    if (selectedUser.value === username) {
      selectedUser.value = null
    }
    addToast(`Logs for ${username} have been cleared`, { type: 'info', duration: 3000 })
  }
})

if (!auth.state.loaded) {
  auth.bootstrapSession()
}
</script>

<template>
  <div class="flex flex-col md:flex-row h-[calc(100vh-70px)] bg-[#fafafa] dark:bg-[#000000] overflow-hidden font-sans text-[#171717] dark:text-[#ffffff]">
    <!-- Sidebar -->
    <aside
      class="fixed md:relative z-30 md:z-auto h-full bg-[#ffffff] dark:bg-[#000000] border-r border-neutral-200/80 dark:border-neutral-800/80 transition-all duration-300 overflow-y-auto"
      :class="[
        sidebarVisible ? 'translate-x-0' : '-translate-x-full md:translate-x-0',
        'w-72 md:w-80'
      ]"
    >
      <div class="p-6 border-b border-neutral-200/80 dark:border-neutral-800/80 flex items-center justify-between">
        <h2 class="font-bold text-xl tracking-tight">Stream</h2>
        <button @click="sidebarVisible = false" class="block md:hidden p-2 hover:bg-neutral-50 dark:hover:bg-neutral-900 rounded-md border border-neutral-200 dark:border-neutral-800 transition-colors">
          Close
        </button>
      </div>

      <div class="flex-1 overflow-y-auto p-4 space-y-2">
        <div 
          v-for="user in Object.values(users)" 
          :key="user.name"
          @click="selectUser(user.name)"
          :class="[
            'group flex items-center gap-4 p-3 rounded-md cursor-pointer transition-all',
            selectedUser === user.name ? 'bg-neutral-100 text-[#171717] dark:bg-neutral-900 dark:text-[#ffffff] ring-1 ring-neutral-200 dark:ring-neutral-800' : 'hover:bg-neutral-50 dark:hover:bg-neutral-900/50'
          ]"
        >
          <div class="relative">
            <img :src="user.avatar" alt="Avatar" class="w-10 h-10 rounded-md object-cover border border-neutral-200 dark:border-neutral-800">
            <span class="absolute bottom-0 right-0 w-3 h-3 bg-emerald-500 border-2 border-[#ffffff] dark:border-[#000000] rounded-full"></span>
          </div>
          <div class="min-w-0">
            <p class="font-semibold truncate">{{ user.name }}</p>
            <p class="text-xs text-neutral-500 dark:text-neutral-400">{{ user.logs.length }} events</p>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main -->
    <main class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <header class="h-16 md:h-20 flex items-center justify-between px-8 bg-[#ffffff]/90 dark:bg-[#000000]/90 border-b border-neutral-200/80 dark:border-neutral-800/80 backdrop-blur-md z-10">
        <div class="flex items-center gap-4">
          <button @click="sidebarVisible = !sidebarVisible" class="p-2 hover:bg-neutral-50 dark:hover:bg-neutral-900 rounded-md border border-neutral-200 dark:border-neutral-800 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg>
          </button>
          <div>
            <h1 class="text-sm md:text-lg font-bold flex flex-wrap items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              {{ route.query.room || 'No Room Selected' }}
            </h1>
            <div class="flex items-center gap-3 text-xs text-neutral-500 dark:text-neutral-400 font-medium">
              <span class="flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                {{ viewers.length }} watching
              </span>
              <span class="px-2 py-0.5 rounded-md bg-neutral-100 dark:bg-neutral-900 text-neutral-600 dark:text-neutral-400 uppercase tracking-widest text-[10px]">
                {{ roomInfo?.visibility || 'private' }}
              </span>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <button @click="loadRoom(false)" class="bg-[#171717] text-[#ffffff] dark:bg-[#ffffff] dark:text-[#000000] hover:bg-neutral-800 dark:hover:bg-neutral-100 rounded-md px-4 py-2 text-sm font-medium transition-colors">
            {{ route.query.room ? 'Switch Room' : 'Join Room' }} 
          </button>
          <button @click="openSettings" class="p-2 border border-neutral-200 dark:border-neutral-800 rounded-md hover:bg-neutral-50 dark:hover:bg-neutral-900 bg-[#ffffff] dark:bg-[#000000] transition-colors">
             <svg viewBox="0 0 24 24" class="w-5 h-5 text-neutral-600 dark:fill-neutral-300 fill-neutral-700 dark:stroke-neutral-300 stroke-neutral-700" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
            </svg>
          </button>
        </div>
      </header>

      <section class="px-8 py-3 bg-[#ffffff] dark:bg-[#000000] border-b border-neutral-200/80 dark:border-neutral-800/80">
        <div class="flex flex-wrap items-center gap-3">
          <div class="relative flex-1 max-w-xs">
            <input v-model="filter.module" type="text" placeholder="Filter by module..." class="w-full pl-9 pr-4 py-2 bg-[#ffffff] dark:bg-[#000000] border border-neutral-200 dark:border-neutral-700 rounded-md text-sm outline-none focus:ring-1 focus:ring-neutral-400 focus:border-neutral-400" />
            <svg class="w-4 h-4 absolute left-3 top-3 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
          </div>
          <div class="relative flex-1 max-w-sm">
            <input v-model="filter.message" type="text" placeholder="Filter by log message..." class="w-full pl-9 pr-4 py-2 bg-[#ffffff] dark:bg-[#000000] border border-neutral-200 dark:border-neutral-700 rounded-md text-sm outline-none focus:ring-1 focus:ring-neutral-400 focus:border-neutral-400" />
            <svg class="w-4 h-4 absolute left-3 top-3 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 16l2.879-2.879m0 0a3 3 0 104.243-4.242 3 3 0 00-4.243 4.242zM21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          </div>
          <div class="relative flex-1 max-w-sm">
            <input v-model="filter.timestamp" type="datetime-local" class="w-full pl-9 pr-4 py-2 bg-[#ffffff] dark:bg-[#000000] border border-neutral-200 dark:border-neutral-700 rounded-md text-sm outline-none focus:ring-1 focus:ring-neutral-400 focus:border-neutral-400" />
            <span class="w-4 h-4 absolute left-3 top-2.5 text-neutral-400 font-mono">>=</span>
          </div>
          <button @click="clearLogs" class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md text-sm font-medium transition-colors">
            Clear Logs
          </button>
        </div>
      </section>

      <!-- Logs Area -->
      <div class="flex-1 overflow-y-auto px-6 py-6 space-y-8 bg-[#ffffff] dark:bg-[#000000]" v-if="selectedUser && users[selectedUser]">
        <div v-for="level in getActiveLevels()" :key="level" class="space-y-3">
          <!-- Level Header -->
          <details open>
            <summary
              class="sticky top-0 z-10 flex items-center justify-between px-5 py-2 rounded-md text-white font-medium shadow-sm cursor-pointer"
              :class="logGroupStyles[level] || logGroupStyles.DEFAULT"
            >
              <div class="flex items-center gap-3">
                <!-- <span class="text-lg">📌</span> -->
                <span>{{ level }} Logs</span>
              </div>
              <span class="text-sm opacity-90">
                {{ getLogsByLevel(level).length }} entries
              </span>
            </summary>

            <!-- Log Cards -->
            <div class="space-y-3 mt-3">
              <div
                v-for="log in getLogsByLevel(level)"
                :key="log.timestamp.getTime()"
                class="bg-[#ffffff] dark:bg-[#0b0a0a] border border-neutral-200/60 dark:border-neutral-800/60 hover:border-neutral-300 dark:hover:border-neutral-700 rounded-md transition-all p-4 shadow-none"
              >
                <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                  <div class="flex-1">
                    <div class="flex items-center gap-3 mb-3">
                      <div class="text-xs font-mono bg-neutral-50 border border-neutral-200 text-neutral-600 dark:bg-neutral-900 dark:border-neutral-800 dark:text-neutral-400 px-3 py-1 rounded-md">
                        {{ log.module || 'unknown' }}
                      </div>
                      <div class="text-xs text-neutral-500 dark:text-neutral-400 font-medium">
                        {{ formatTimestamp(log.timestamp) }}
                      </div>
                    </div>

                    <p class="text-[#171717] dark:text-[#ffffff] leading-relaxed font-mono text-sm whitespace-pre-wrap">
                      {{ log.message }}
                    </p>
                  </div>

                  <button 
                    @click="copyToClipboard(log.message, $event)"
                    class="text-xs px-3 py-1.5 bg-neutral-50 border border-neutral-200 text-neutral-600 hover:bg-neutral-100 dark:bg-neutral-900 dark:border-neutral-800 dark:text-neutral-400 dark:hover:bg-neutral-800/80 rounded-md transition-colors flex items-center gap-1"
                  >
                    📋 Copy
                  </button>
                </div>
              </div>
            </div>
          </details>
        </div>

        <div v-if="filteredLogs.length === 0" class="text-center py-20 text-neutral-500">
          <p class="text-6xl mb-4">🔍</p>
          <p class="mb-4">No logs match your current filters</p>
          <button @click="sendATestLog" class="bg-[#171717] text-[#ffffff] dark:bg-[#ffffff] dark:text-[#000000] hover:bg-neutral-800 dark:hover:bg-neutral-100 px-4 py-2 rounded-md font-medium transition-colors">
            Send a test log
          </button>
        </div>
      </div>

      <div v-if="Object.keys(users).length === 0" class="flex-1 flex flex-col gap-4 items-center justify-center text-neutral-400">
        <div class="text-center">
          <p class="text-7xl mb-6">👻</p>
          <p class="text-xl">No users have sent logs yet</p>
        </div>
        <button @click="sendATestLog" class="bg-[#171717] text-[#ffffff] dark:bg-[#ffffff] dark:text-[#000000] hover:bg-neutral-800 dark:hover:bg-neutral-100 px-4 py-2 rounded-md font-medium transition-colors">
          Send a test log
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="!selectedUser" class="flex-1 flex items-center justify-center text-neutral-400">
        <div class="text-center">
          <p class="text-7xl mb-6">📭</p>
          <p class="text-xl">Select a user to view their logs</p>
        </div>
      </div>
    </main>

    <transition name="slide">
      <aside v-if="showSettings" class="fixed inset-y-0 right-0 w-96 bg-[#ffffff] dark:bg-[#000000] border-l border-neutral-200/80 dark:border-neutral-800/80 shadow-xl z-50 p-8 overflow-y-auto">
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-xl font-bold">Room Settings</h2>
          <button @click="showSettings = false" class="text-neutral-400 hover:text-neutral-900 dark:hover:text-[#ffffff] transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        
        <div class="space-y-6 mb-8">
          <div>
            <label class="text-xs font-bold uppercase text-neutral-400 tracking-widest block mb-4">Manage Access</label>
            <div class="space-y-3">
              <input v-model="shareUsername" type="text" placeholder="Username" class="w-full px-4 py-3 bg-[#ffffff] dark:bg-[#000000] border border-neutral-200 dark:border-neutral-700 rounded-md text-sm outline-none focus:ring-1 focus:ring-neutral-400 focus:border-neutral-400" />
              <div class="flex items-center justify-between">
                <span class="text-sm">Allow Write Access</span>
                <input v-model="shareCanWrite" type="checkbox" class="w-5 h-5 accent-[#171717] dark:accent-[#ffffff]" />
              </div>
              <button @click="shareRoom" class="w-full py-3 bg-[#171717] text-[#ffffff] dark:bg-[#ffffff] dark:text-[#000000] hover:bg-neutral-800 dark:hover:bg-neutral-100 rounded-md font-medium transition-colors">Invite User</button>
            </div>
          </div>

          <div class="pt-6 border-t border-neutral-200 dark:border-neutral-800">
            <label class="text-xs font-bold uppercase text-neutral-400 tracking-widest block mb-4">Visibility</label>
            <div class="grid grid-cols-2 gap-3">
              <button @click="updateVisibility('private')" :class="roomInfo?.visibility === 'private' ? 'bg-[#171717] text-[#ffffff] dark:bg-[#ffffff] dark:text-[#000000]' : 'bg-neutral-100 dark:bg-neutral-900 text-neutral-500 hover:bg-neutral-200 dark:hover:bg-neutral-800'" class="py-3 rounded-md text-sm font-medium transition-colors">Private</button>
              <button @click="updateVisibility('public')" :class="roomInfo?.visibility === 'public' ? 'bg-[#171717] text-[#ffffff] dark:bg-[#ffffff] dark:text-[#000000]' : 'bg-neutral-100 dark:bg-neutral-900 text-neutral-500 hover:bg-neutral-200 dark:hover:bg-neutral-800'" class="py-3 rounded-md text-sm font-medium transition-colors">Public</button>
            </div>
          </div>
        </div>
        <section class="space-y-3 rounded-md border border-neutral-200 p-4 dark:border-neutral-800">
          <div class="text-sm font-semibold text-[#171717] dark:text-[#ffffff]">Shared with</div>
          <div v-if="roomInfo?.shared_with?.length" class="space-y-2">
            <div
              v-for="entry in roomInfo.shared_with"
              :key="entry.username"
              class="flex items-center justify-between gap-3 rounded-md bg-neutral-50 border border-neutral-200 p-3 dark:bg-neutral-900 dark:border-neutral-800"
            >
              <div class="min-w-0">
                <div class="truncate text-sm font-medium text-[#171717] dark:text-[#ffffff]">{{ entry.username }}</div>
                <div class="text-xs text-neutral-500 dark:text-neutral-400">{{ entry.can_write ? 'Can write' : 'Read only' }}</div>
              </div>
              <button class="rounded-md border border-red-200 dark:border-red-900/50 px-3 py-1 text-xs font-medium text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-950/20 transition-colors" @click="unshareRoom(entry.username)">
                Remove
              </button>
            </div>
          </div>
          <div v-else class="text-sm text-neutral-500 dark:text-neutral-400">
            No shared users yet.
          </div>
        </section>
      </aside>
    </transition>
  </div>
</template>

<style scoped>
.btn-primary {
  background: #171717;
  color: white;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s;
}

.dark .btn-primary {
  background: white;
  color: black;
}

.btn-primary:hover {
  opacity: 0.9;
}

.slide-enter-active, .slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from, .slide-leave-to {
  transform: translateX(100%);
}
</style>
