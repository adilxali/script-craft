<template>
  <AppShell @open-command-palette="isCmdPaletteOpen = true">
    <CommandPalette :is-open="isCmdPaletteOpen" @close="isCmdPaletteOpen = false" @open="isCmdPaletteOpen = true" />

    <div class="bg-white rounded-[28px] border border-[#F2D8D2] shadow-soft overflow-hidden h-[calc(100vh-10rem)] min-h-[550px] flex flex-col">
      <!-- Toolbar -->
      <div class="px-4 py-2.5 bg-[#FFF7F4] border-b border-[#F2D8D2] flex items-center justify-between shrink-0">
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-1 bg-white p-1 rounded-xl border border-[#F2D8D2]">
            <button
              v-for="file in files"
              :key="file.name"
              @click="activeFileName = file.name"
              :class="[
                'px-3 py-1.5 rounded-lg text-xs font-mono transition-all flex items-center gap-2',
                activeFileName === file.name
                  ? 'bg-[#E76A4D] text-white font-bold shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              ]"
            >
              <FileCode class="w-3.5 h-3.5" />
              <span>{{ file.name }}</span>
            </button>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <button
            @click="copyShareLink"
            class="px-3.5 py-1.5 rounded-xl bg-white border border-[#F2D8D2] hover:bg-[#FFF7F4] text-slate-700 text-xs font-semibold transition-colors flex items-center gap-1.5 shadow-sm"
          >
            <Share2 class="w-3.5 h-3.5 text-[#E76A4D]" />
            <span>{{ copyNotice || 'Share Code' }}</span>
          </button>

          <button
            @click="runPlaygroundCode"
            :disabled="isExecuting"
            class="px-5 py-1.5 rounded-xl bg-[#E76A4D] hover:bg-[#D85D3E] text-white font-extrabold text-xs shadow-md shadow-[#E76A4D]/20 transition-all flex items-center gap-1.5"
          >
            <Play class="w-3.5 h-3.5 fill-white" />
            <span>{{ isExecuting ? 'Running...' : 'Run Code (⌘↵)' }}</span>
          </button>
        </div>
      </div>

      <!-- Editor + Console Grid -->
      <div class="flex-1 flex flex-col lg:flex-row overflow-hidden p-3 gap-3">
        <div class="flex-1 h-full min-h-[350px]">
          <MonacoEditor
            v-model="activeFileCode"
            :filename="activeFileName"
            @reset="resetActiveFile"
            @run="runPlaygroundCode"
          />
        </div>

        <div class="w-full lg:w-[480px] h-full">
          <ConsolePanel
            :logs="logs"
            :return-value="returnValue"
            :runtime-ms="runtimeMs"
            :status="executionStatus"
            :error="executionError"
            @clear="logs = []"
          />
        </div>
      </div>
    </div>
  </AppShell>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { FileCode, Share2, Play } from 'lucide-vue-next'
import AppShell from '~/components/layout/AppShell.vue'
import CommandPalette from '~/components/ui/CommandPalette.vue'
import MonacoEditor from '~/components/ide/MonacoEditor.client.vue'
import ConsolePanel from '~/components/ide/ConsolePanel.vue'
import { executeJSCode, type LogEntry } from '~/utils/worker-runner'

definePageMeta({
  middleware: 'auth'
})

const isCmdPaletteOpen = ref(false)

const files = ref([
  {
    name: 'index.js',
    content: `// Standalone JavaScript Playground Engine
// Write any JavaScript code, functions, promises, or async tasks here!

function calculateStats(numbers) {
  const sum = numbers.reduce((acc, n) => acc + n, 0);
  const avg = sum / numbers.length;
  return { sum, avg, count: numbers.length };
}

const data = [10, 20, 30, 40, 50];
console.log("Input Array:", data);
console.log("Calculated Stats:", calculateStats(data));
`
  },
  {
    name: 'utils.js',
    content: `// Helper Utility functions
function formatDate(date) {
  return new Date(date).toLocaleDateString();
}

console.log("Current Date:", formatDate(Date.now()));
`
  }
])

const activeFileName = ref('index.js')

const activeFileCode = computed({
  get: () => {
    const f = files.value.find(file => file.name === activeFileName.value)
    return f ? f.content : ''
  },
  set: (val: string) => {
    const f = files.value.find(file => file.name === activeFileName.value)
    if (f) f.content = val
    if (import.meta.client) {
      localStorage.setItem('scriptcraft_playground_' + activeFileName.value, val)
    }
  }
})

const isExecuting = ref(false)
const logs = ref<LogEntry[]>([])
const returnValue = ref<any>(undefined)
const runtimeMs = ref(0)
const executionStatus = ref<'idle' | 'running' | 'completed' | 'error'>('idle')
const executionError = ref<string | undefined>(undefined)

const copyNotice = ref('')

async function runPlaygroundCode() {
  isExecuting.value = true
  executionStatus.value = 'running'
  executionError.value = undefined

  const res = await executeJSCode(activeFileCode.value)

  logs.value = res.logs
  returnValue.value = res.returnValue
  runtimeMs.value = res.runtimeMs
  executionError.value = res.error

  isExecuting.value = false
  if (res.error) {
    executionStatus.value = 'error'
  } else {
    executionStatus.value = 'completed'
  }
}

function resetActiveFile() {
  if (activeFileName.value === 'index.js') {
    activeFileCode.value = `console.log("Hello from ScriptCraft Playground!");`
  } else {
    activeFileCode.value = `// Clean file`
  }
  logs.value = []
  returnValue.value = undefined
  executionStatus.value = 'idle'
}

function copyShareLink() {
  if (import.meta.client) {
    navigator.clipboard.writeText(window.location.href)
    copyNotice.value = 'Copied Link!'
    setTimeout(() => {
      copyNotice.value = ''
    }, 2000)
  }
}

onMounted(() => {
  if (import.meta.client) {
    files.value.forEach(f => {
      const saved = localStorage.getItem('scriptcraft_playground_' + f.name)
      if (saved) f.content = saved
    })
  }
})
</script>
