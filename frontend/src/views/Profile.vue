<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { auth } from '@/stores/auth'
import { apiDelete, apiGet, apiPost, apiPut } from '@/stores/api'
import { useDialog } from '@/components/useDialog'
import router from '@/router'
import { addToast } from '@/components/Toast.vue'

const user = computed(() => auth.state.user)
const provider = computed(() => auth.state.provider)
const route = useRoute()
const keyLabel = ref('')
const apiKeys = ref([])
const generating = ref(false)
const keyError = ref('')
const newKeyValue = ref('')
const rooms = ref([])
const roomsLoading = ref(false)
const roomsError = ref('')
const personalRoomName = ref('')
const personalRoomVisibility = ref('private')
const creatingPersonalRoom = ref(false)
const orgs = ref([])
const orgActionError = ref('')
const activeOrg = ref('')
const memberUsername = ref('')
const memberRole = ref('developer')
const orgRoomName = ref('')
const orgRoomVisibility = ref('private')
const dialog = useDialog();
const activeTab = ref('account')

const tabs = [
  { id: 'account', label: 'Account', icon: '👤' },
  { id: 'keys', label: 'API Keys', icon: '🔑' },
  { id: 'rooms', label: 'Rooms', icon: '🗂️' },
  { id: 'orgs', label: 'Organizations', icon: '🏢' },
]

const canCreatePersonalRooms = ref(true);

const actions = {
  create: {
    room: async (value) => {
      activeTab.value = 'rooms'
      personalRoomName.value = value || ''
    },
    apiKey: async (value) => {
      activeTab.value = 'keys'
      keyLabel.value = value || 'Default key'
      await generateApiKey()
      router.replace({ query: {} })
    },
    org: async (value) => {
      try {
        activeTab.value = 'orgs'
        await apiPost('/orgs', { name: value })
        router.replace({ query: {} })
        addToast(`Organisation "${value}" created successfully!`, { type: 'success', duration: 5000 })
      } catch (error) {
        addToast(error.message || 'Could not create organisation', { type: 'error', duration: 5000 })
      }
    },
  },
  delete: {
    apiKey: async (value) => {
      activeTab.value = 'keys'
      await revokeApiKey(value)
      router.replace({ query: {} })
    },
    room: async (value) => {
      try {
        activeTab.value = 'orgs'
        await apiDelete(`/rooms/${encodeURIComponent(value)}`)
        router.replace({ query: {} })
        addToast(`Room "${value}" deleted successfully!`, { type: 'success', duration: 5000 })
      } catch (error) {
        addToast(error.message || 'Could not delete room', { type: 'error', duration: 5000 })
      }
    },
    org: async (value) => {
      try {
        activeTab.value = 'orgs'
        await apiDelete(`/orgs/${encodeURIComponent(value)}`)
        router.replace({ query: {} })
        addToast(`Organisation "${value}" deleted successfully!`, { type: 'success', duration: 5000 })
      } catch (error) {
        addToast(error.message || 'Could not delete organisation', { type: 'error', duration: 5000 })
      }
    },
  },
}

if (route.query.action && route.query.key && route.query.value) {
  (actions[route.query.action]?.[route.query.key])(route.query.value)
}

async function loadApiKeys() {
  try {
    keyError.value = ''
    const payload = await apiGet('/auth/api-keys')
    apiKeys.value = payload.keys || []
  } catch (error) {
    keyError.value = error.message || 'Could not load API keys'
  }
}

async function generateApiKey() {
  generating.value = true
  keyError.value = ''
  newKeyValue.value = ''

  try {
    const payload = await apiPost('/auth/api-keys', { label: keyLabel.value || 'Default key' })
    newKeyValue.value = payload.api_key || ''
    keyLabel.value = ''
    await loadApiKeys()
  } catch (error) {
    keyError.value = error.message || 'Could not create API key'
  } finally {
    generating.value = false
  }
}

async function revokeApiKey(keyId) {
  try {
    keyError.value = ''
    await apiDelete(`/auth/api-keys/${encodeURIComponent(keyId)}`)
    await loadApiKeys()
  } catch (error) {
    keyError.value = error.message || 'Could not revoke API key'
  }
}

async function loadRooms() {
  roomsLoading.value = true
  roomsError.value = ''
  try {
    const payload = await apiGet('/rooms')
    rooms.value = payload.rooms || []
  } catch (error) {
    roomsError.value = error.message || 'Could not load rooms'
  } finally {
    roomsLoading.value = false
  }
}

function formatBytes(value) {
  const bytes = Number(value || 0)
  if (!Number.isFinite(bytes) || bytes <= 0) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  const exp = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1)
  const size = bytes / (1024 ** exp)
  return `${size.toFixed(size >= 10 || exp === 0 ? 0 : 1)} ${units[exp]}`
}

async function createRoom(type = 'personal') {
  const isPersonal = type === 'personal'
  const roomNameRef = isPersonal ? personalRoomName : orgRoomName
  const visibilityRef = isPersonal ? personalRoomVisibility : orgRoomVisibility
  const errorRef = isPersonal ? roomsError : orgActionError

  const roomName = roomNameRef.value.trim()
  if (!roomName) {
    errorRef.value = 'Room name is required'
    return
  }

  if (!isPersonal && !activeOrg.value) {
    return
  }

  if (isPersonal) {
    creatingPersonalRoom.value = true
  }

  errorRef.value = ''
  try {
    await apiPost(isPersonal ? '/rooms' : `/rooms?org_name=${encodeURIComponent(activeOrg.value)}`, {
      room: roomName,
      visibility: visibilityRef.value,
    })

    roomNameRef.value = ''
    visibilityRef.value = 'private'

    if (isPersonal) {
      await loadRooms()
    }

    const { confirmed } = await dialog.confirm(
      isPersonal
        ? 'Room created successfully! Open it now?'
        : 'Room created successfully! Would you like to view the room now?'
    )
    if (confirmed) {
      router.push({ name: 'logs', query: { room: roomName } })
    }
  } catch (error) {
    errorRef.value = error.message || 'Could not create room'
  } finally {
    if (isPersonal) {
      creatingPersonalRoom.value = false
    }
  }
}

async function loadOrgs() {
  try {
    orgActionError.value = ''
    const payload = await apiGet('/orgs')
    orgs.value = payload.organisations || []
    if (!activeOrg.value && orgs.value.length > 0) {
      activeOrg.value = orgs.value[0].name
    }
  } catch (error) {
    orgActionError.value = error.message || 'Could not load organisations'
  }
}

async function createOrg() {
  const { confirmed, data } = await dialog.input("Organisation Name", [
    {
      label: "Name",
      name: "name",
      type: "text",
      placeholder: "Enter organisation name",
      required: true,
    },
  ]);
  if (confirmed && data.name) {
    try {
      await apiPost('/orgs', { name: data.name });
      await loadOrgs();
    } catch (error) {
      const detail = Array.isArray(error.detail) ? error.detail[0].msg : error.detail?.msg || error.detail;
      addToast(detail || 'Could not create organisation', { type: 'error', duration: 5000 });
    }
  }
}

async function inviteMember() {
  if (!activeOrg.value) {
    return
  }
  try {
    orgActionError.value = ''
    await apiPost(`/orgs/${encodeURIComponent(activeOrg.value)}/members`, {
      username: memberUsername.value,
      role: memberRole.value,
    })
    memberUsername.value = ''
    memberRole.value = 'developer'
    await loadOrgs()
  } catch (error) {
    orgActionError.value = error.message || 'Could not invite member'
  }
}

const selectedOrg = computed(() => orgs.value.find((org) => org.name === activeOrg.value) || null)

async function copyKey(event) {
  if (!newKeyValue.value) {
    return
  }
  const button = event.currentTarget
  button.textContent = '✅ Copied'
  button.classList.add('bg-green-800', 'text-white')
  await navigator.clipboard.writeText(newKeyValue.value)
  setTimeout(() => {
    button.classList.remove('bg-green-800', 'text-white')
    button.textContent = 'Copy key'
  }, 3000);
}

onMounted(async () => {
  if (!auth.state.loaded) {
    await auth.bootstrapSession()
  }

  if (!auth.state.user?.username) {
    router.replace('/auth/login')
    return
  }

  await Promise.all([loadApiKeys(), loadRooms(), loadOrgs()])
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 font-sans text-slate-900 dark:text-slate-100">
    <div class="mx-auto max-w-5xl px-6 py-12">
      
      <header class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10">
        <div class="flex items-center gap-5">
          <div v-if="!user?.avatar_url" class="h-20 w-20 flex items-center justify-center rounded-3xl bg-gradient-to-br from-indigo-500 to-purple-600 text-2xl font-bold text-white shadow-xl shadow-indigo-500/20">
            {{ (user?.username || '?').slice(0, 2).toUpperCase() }}
          </div>
          <img v-else :src="user?.avatar_url" class="h-20 w-20 rounded-3xl object-cover shadow-xl" />
          
          <div>
            <h1 class="text-3xl font-black tracking-tight">{{ user?.display_name || user?.username }}</h1>
            <p class="text-slate-500 font-medium">{{ user?.email || 'Personal Account' }}</p>
          </div>
        </div>
      </header>

      <nav class="flex items-center justify-between bg-white dark:bg-slate-900 p-1.5 rounded-2xl border border-slate-200 dark:border-slate-800 mb-8 shadow-sm overflow-x-auto">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-bold transition-all whitespace-nowrap',
            activeTab === tab.id 
              ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 shadow-lg' 
              : 'text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-800'
          ]"
        >
          <span>{{ tab.icon }}</span>
          {{ tab.label }}
        </button>
      </nav>

      <main class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm min-h-[400px] overflow-hidden">
        
        <section v-if="activeTab === 'account'" class="p-8 animate-in fade-in slide-in-from-bottom-2 duration-300">
          <h3 class="text-xl font-bold mb-6">Profile Details</h3>
          <div class="grid md:grid-cols-2 gap-6">
            <div v-for="(label, key) in { 'Username': user?.username, 'Provider': provider, 'Display Name': user?.display_name, 'Email': user?.email }" :key="key" 
                 class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700/50">
              <p class="text-[10px] uppercase tracking-widest font-black text-slate-400 mb-1">{{ key }}</p>
              <p class="font-mono text-sm">{{ label || '—' }}</p>
            </div>
          </div>
        </section>

        <section v-if="activeTab === 'keys'" class="p-8 animate-in fade-in slide-in-from-bottom-2 duration-300">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h3 class="text-xl font-bold">API Access</h3>
              <p class="text-sm text-slate-500">Manage keys for external integration.</p>
            </div>
          </div>

          <div class="flex gap-3 mb-8">
            <input v-model="keyLabel" type="text" placeholder="Key label..." class="flex-1 px-4 py-3 bg-slate-50 dark:bg-slate-800 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500" />
            <button @click="generateApiKey" :disabled="generating" class="px-6 py-3 bg-indigo-600 text-white rounded-xl font-bold hover:bg-indigo-500 disabled:opacity-50">
              {{ generating ? 'Generating...' : 'New Key' }}
            </button>
          </div>

          <p v-if="keyError" class="mt-3 rounded-xl border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:border-rose-500/40 dark:bg-rose-500/10 dark:text-rose-300">
            {{ keyError }}
          </p>
          <div v-if="newKeyValue" class="m-4 rounded-xl border border-amber-300 bg-amber-50 p-4 dark:border-amber-500/40 dark:bg-amber-500/10">
            <p class="text-sm font-semibold text-amber-800 dark:text-amber-300">Copy this key now. It will not be shown again.</p>
            <p class="mt-2 break-all rounded-lg bg-white px-3 py-2 font-mono text-xs text-slate-900 dark:bg-slate-900 dark:text-amber-100">{{ newKeyValue }}</p>
            <button
              type="button"
              @click="copyKey"
              class="mt-3 rounded-lg border border-amber-400 px-3 py-1 text-sm font-medium text-amber-800 transition hover:bg-amber-100 dark:border-amber-400/50 dark:text-amber-200 dark:hover:bg-amber-500/10"
            >
              Copy key
            </button>
          </div>

          <div class="space-y-3">
            <div v-for="key in apiKeys" :key="key.id" class="flex items-center justify-between p-4 border border-slate-100 dark:border-slate-800 rounded-2xl hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
              <div>
                <p class="font-bold text-sm">{{ key.label || 'Unnamed Key' }}</p>
                <code class="text-xs text-indigo-500">{{ key.key_preview }}</code>
              </div>
              <button @click="revokeApiKey(key.id)" class="text-xs font-bold text-red-500 hover:underline">Revoke</button>
            </div>
          </div>
        </section>

        <section v-if="activeTab === 'rooms'" class="p-8 animate-in fade-in slide-in-from-bottom-2 duration-300">
          <div class="flex items-center justify-between gap-4 mb-6">
            <div>
              <h3 class="text-xl font-bold">Rooms</h3>
              <p class="text-sm text-slate-500">Browse rooms you can access and create rooms.</p>
            </div>
            <button
              type="button"
              @click="loadRooms"
              class="rounded-xl bg-slate-300 px-4 py-2 text-sm font-semibold text-slate-900 transition hover:bg-slate-200 dark:bg-slate-700 dark:text-white dark:hover:bg-slate-600"
            >
              Refresh
            </button>
          </div>

          <div class="mb-6 rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
            <p class="text-sm font-semibold text-slate-900 dark:text-white">Create personal room</p>
            <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">Current plan: <span class="font-bold uppercase">{{ currentPlan }}</span></p>

            <div class="mt-3 grid gap-3 md:grid-cols-[1fr_auto_auto]">
              <input
                v-model="personalRoomName"
                :disabled="!canCreatePersonalRooms || creatingPersonalRoom"
                type="text"
                placeholder="Room ID"
                class="w-full rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm text-slate-900 outline-none focus:border-cyan-500 disabled:cursor-not-allowed disabled:opacity-60 dark:border-slate-600 dark:bg-slate-900 dark:text-white"
              />
              <!--select an org to own room -->
              <select
                v-if="orgs.length > 0"
                v-model="activeOrg"
                :disabled="!canCreatePersonalRooms || creatingPersonalRoom"
                class="rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 outline-none focus:border-cyan-500 disabled:cursor-not-allowed disabled:opacity-60 dark:border-slate-600 dark:bg-slate-900 dark:text-white"
              >
                <option value="" selected>Personal room</option>
                <option v-for="org in orgs" :key="org.name" :value="org.name">Org: {{ org.name }}</option>
              </select>
              <select
                v-model="personalRoomVisibility"
                :disabled="!canCreatePersonalRooms || creatingPersonalRoom"
                class="rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 outline-none focus:border-cyan-500 disabled:cursor-not-allowed disabled:opacity-60 dark:border-slate-600 dark:bg-slate-900 dark:text-white"
              >
                <option value="private">private</option>
                <option value="public">public</option>
              </select>
              <button
                type="button"
                :disabled="!canCreatePersonalRooms || creatingPersonalRoom"
                @click="createRoom('personal')"
                class="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {{ creatingPersonalRoom ? 'Creating...' : 'Create room' }}
              </button>
            </div>

            <p v-if="!canCreatePersonalRooms" class="mt-2 text-xs text-amber-700 dark:text-amber-300">
              Upgrade to Pro or Team to create additional personal rooms.
            </p>
          </div>

          <p v-if="roomsError" class="mb-4 rounded-xl border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:border-rose-500/40 dark:bg-rose-500/10 dark:text-rose-300">
            {{ roomsError }}
          </p>

          <p v-if="roomsLoading" class="text-sm text-slate-500 dark:text-slate-400">Loading rooms...</p>

          <div v-else class="space-y-3">
            <div
              v-for="room in rooms"
              :key="room.room"
              class="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-900/70 md:flex-row md:items-center md:justify-between"
            >
              <div>
                <p class="font-bold text-slate-900 dark:text-white">{{ room.room }}</p>
                <div class="mt-1 flex flex-wrap items-center gap-2 text-xs">
                  <span class="rounded-full bg-slate-100 px-2 py-1 text-slate-700 dark:bg-slate-800 dark:text-slate-200">{{ room.owner_type }}:{{ room.owner_id }}</span>
                  <span class="rounded-full bg-cyan-100 px-2 py-1 text-cyan-700 dark:bg-cyan-500/20 dark:text-cyan-200">{{ room.visibility }}</span>
                  <span class="rounded-full bg-indigo-100 px-2 py-1 text-indigo-700 dark:bg-indigo-500/20 dark:text-indigo-200">{{ room.room_type }}</span>
                  <span class="rounded-full bg-emerald-100 px-2 py-1 text-emerald-700 dark:bg-emerald-500/20 dark:text-emerald-200">{{ formatBytes(room.max_log_size) }} cap</span>
                </div>
              </div>

              <div class="flex items-center gap-2">
                <span class="text-xs font-semibold" :class="room.can_write ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-500 dark:text-slate-400'">
                  {{ room.can_write ? 'write access' : 'read only' }}
                </span>
                <button
                  type="button"
                  @click="router.push({ name: 'logs', query: { room: room.room } })"
                  class="rounded-xl bg-slate-900 px-3 py-2 text-xs font-semibold text-white transition hover:bg-slate-700 dark:bg-white dark:text-slate-900 dark:hover:bg-slate-200"
                >
                  Open
                </button>
              </div>
            </div>

            <p v-if="rooms.length === 0" class="rounded-xl border border-dashed border-slate-300 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
              No accessible rooms found yet.
            </p>
          </div>
        </section>

        <section v-if="activeTab === 'orgs'" class="p-8 animate-in fade-in slide-in-from-bottom-2 duration-300">
          <h2 class="text-xl font-semibold text-slate-900 dark:text-white">Organisations</h2>
          <p class="mt-2 text-sm text-slate-500 dark:text-slate-300">Team plan users can invite members to their orgs, and create org rooms.</p>

          <div class="mt-4">
            <label class="mb-1 block text-xs uppercase tracking-[0.12em] text-slate-500 dark:text-slate-400">Selected org</label>
            <select
              v-model="activeOrg"
              class="w-full rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm text-slate-900 outline-none focus:border-cyan-500 dark:border-slate-600 dark:bg-slate-900 dark:text-white"
            >
              <option value="">Select organisation</option>
              <option v-for="org in orgs" :key="org.name" :value="org.name">{{ org.name }}</option>
            </select>
          </div>

          <div v-if="selectedOrg" class="mt-4 grid gap-4 sm:grid-cols-2">
            <div class="rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-900/70">
              <p class="text-sm font-semibold text-slate-900 dark:text-white">Invite member</p>
              <input
                v-model="memberUsername"
                type="text"
                placeholder="Username"
                class="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 outline-none focus:border-cyan-500 dark:border-slate-600 dark:bg-slate-900 dark:text-white"
              />
              <select
                v-model="memberRole"
                class="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 outline-none focus:border-cyan-500 dark:border-slate-600 dark:bg-slate-900 dark:text-white"
              >
                <option value="viewer">viewer</option>
                <option value="developer">developer</option>
                <option value="admin">admin</option>
              </select>
              <button
                type="button"
                @click="inviteMember"
                class="mt-2 rounded-xl bg-emerald-600 px-3 py-2 text-sm font-semibold text-white transition hover:bg-emerald-500"
              >
                Invite
              </button>
            </div>

            <div class="rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-900/70">
              <p class="text-sm font-semibold text-slate-900 dark:text-white">Create org room</p>
              <input
                v-model="orgRoomName"
                type="text"
                placeholder="Room ID"
                class="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 outline-none focus:border-cyan-500 dark:border-slate-600 dark:bg-slate-900 dark:text-white"
              />
              <select
                v-model="orgRoomVisibility"
                class="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 outline-none focus:border-cyan-500 dark:border-slate-600 dark:bg-slate-900 dark:text-white"
              >
                <option value="private">private</option>
                <option value="public">public</option>
              </select>
              <button
                type="button"
                @click="createRoom('org')"
                class="mt-2 rounded-xl bg-violet-600 px-3 py-2 text-sm font-semibold text-white transition hover:bg-violet-500"
              >
                Create room
              </button>
            </div>
          </div>

          <div v-if="selectedOrg" class="mt-4 rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-900/70">
            <p class="text-sm font-semibold text-slate-900 dark:text-white">Members</p>
            <ul class="mt-2 space-y-1 text-sm text-slate-600 dark:text-slate-300">
              <li v-for="member in selectedOrg.members || []" :key="member.username || member">
                {{ member.username || member }} <span class="text-xs text-slate-500">({{ member.role || 'member' }})</span>
              </li>
            </ul>
          </div>

          <div class="mt-4 space-y-3">
            <button
              type="button"
              @click="createOrg"
              class="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-cyan-500 w-fit"
            >
              Create organisation
            </button>
          </div>

          <p v-if="orgActionError" class="mt-3 rounded-xl border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:border-rose-500/40 dark:bg-rose-500/10 dark:text-rose-300">
            {{ orgActionError }}
          </p>
        </section>
      </main>

    </div>
  </div>
</template>
