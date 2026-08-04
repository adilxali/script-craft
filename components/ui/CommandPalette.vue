<template>
  <Teleport to="body">
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-slate-950/80 backdrop-blur-md transition-all"
      @click.self="close"
    >
      <div class="w-full max-w-xl bg-slate-900 border border-white/10 rounded-2xl shadow-2xl overflow-hidden flex flex-col">
        <!-- Input Header -->
        <div class="p-4 border-b border-white/10 flex items-center gap-3 bg-slate-950/40">
          <Search class="w-5 h-5 text-emerald-400" />
          <input
            ref="inputRef"
            v-model="query"
            type="text"
            placeholder="Type a command or search lessons... (Esc to close)"
            class="w-full bg-transparent text-white placeholder-slate-500 text-sm focus:outline-none"
            @keydown.esc="close"
          />
          <kbd class="px-2 py-1 rounded bg-slate-800 border border-slate-700 text-[10px] font-mono text-slate-400">
            ESC
          </kbd>
        </div>

        <!-- Navigation items -->
        <div class="max-h-80 overflow-y-auto p-2 space-y-1">
          <div
            v-for="(item, index) in filteredItems"
            :key="index"
            @click="selectItem(item)"
            class="w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-left cursor-pointer hover:bg-emerald-500/10 hover:border-emerald-500/30 border border-transparent transition-all group"
          >
            <div class="flex items-center gap-3">
              <component :is="item.icon" class="w-4 h-4 text-slate-400 group-hover:text-emerald-400 transition-colors" />
              <div>
                <p class="text-sm font-medium text-slate-200 group-hover:text-white">
                  {{ item.title }}
                </p>
                <p class="text-xs text-slate-500">
                  {{ item.subtitle }}
                </p>
              </div>
            </div>
            <span class="text-xs font-mono text-slate-500 group-hover:text-emerald-400">
              {{ item.actionLabel }}
            </span>
          </div>

          <div v-if="filteredItems.length === 0" class="py-8 text-center text-slate-500 text-sm">
            No matching commands found.
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, LayoutDashboard, BookOpen, Code2, Globe, Palette } from 'lucide-vue-next'
import { useLanguageStore } from '~/stores/language'
import { useThemeStore } from '~/stores/theme'

const props = defineProps<{ isOpen: boolean }>()
const emit = defineEmits(['close'])

const router = useRouter()
const languageStore = useLanguageStore()
const themeStore = useThemeStore()

const query = ref('')
const inputRef = ref<HTMLInputElement | null>(null)

const commandItems = [
  {
    title: 'Go to Dashboard',
    subtitle: 'View overall progress, streak counter, and daily challenge',
    icon: LayoutDashboard,
    actionLabel: 'Navigate',
    action: () => router.push('/dashboard')
  },
  {
    title: 'Lesson 1: Closures & Lexical Scope',
    subtitle: 'Module 1 • High-level closures and outer lexical scope',
    icon: BookOpen,
    actionLabel: 'Open Lesson',
    action: () => router.push('/learn/01-foundations/01-closures')
  },
  {
    title: 'Lesson 2: Async Promises & Event Loop',
    subtitle: 'Module 1 • Promises, microtasks, and async/await',
    icon: BookOpen,
    actionLabel: 'Open Lesson',
    action: () => router.push('/learn/01-foundations/02-async-promises')
  },
  {
    title: 'Open Standalone JS Playground',
    subtitle: 'Full-screen Web Worker IDE workspace',
    icon: Code2,
    actionLabel: 'Launch IDE',
    action: () => router.push('/playground')
  },
  {
    title: 'Switch to Hinglish Mode',
    subtitle: 'Explain concepts in conversational Roman Hindi',
    icon: Globe,
    actionLabel: 'Language',
    action: () => languageStore.setLanguage('hi')
  },
  {
    title: 'Switch to English Mode',
    subtitle: 'Explain concepts in standard technical English',
    icon: Globe,
    actionLabel: 'Language',
    action: () => languageStore.setLanguage('en')
  },
  {
    title: 'Set Theme: Tokyo Night',
    subtitle: 'Monaco dark high-contrast theme',
    icon: Palette,
    actionLabel: 'Theme',
    action: () => themeStore.setEditorTheme('tokyo-night')
  },
  {
    title: 'Set Theme: Catppuccin Mocha',
    subtitle: 'Soothing pastel editor theme',
    icon: Palette,
    actionLabel: 'Theme',
    action: () => themeStore.setEditorTheme('catppuccin')
  }
]

const filteredItems = computed(() => {
  if (!query.value.trim()) return commandItems
  const q = query.value.toLowerCase()
  return commandItems.filter(
    item => item.title.toLowerCase().includes(q) || item.subtitle.toLowerCase().includes(q)
  )
})

function close() {
  emit('close')
  query.value = ''
}

function selectItem(item: any) {
  item.action()
  close()
}

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    nextTick(() => {
      inputRef.value?.focus()
    })
  }
})

function handleGlobalKeydown(e: KeyboardEvent) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault()
    if (props.isOpen) {
      close()
    } else {
      emit('open')
    }
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleGlobalKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleGlobalKeydown)
})
</script>
