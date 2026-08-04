<template>
  <div class="my-6 rounded-2xl border border-[#E76A4D]/30 bg-slate-950 overflow-hidden shadow-lg font-sans">
    <!-- Playground Header -->
    <div class="px-4 py-2.5 bg-slate-900 border-b border-white/10 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <Sparkles class="w-4 h-4 text-[#F5A623]" />
        <span class="text-xs font-extrabold text-white tracking-wide uppercase font-mono">
          {{ title || 'Live Interactive Sandbox' }}
        </span>
      </div>

      <button
        @click="runInlineCode"
        :disabled="isRunning"
        class="px-3.5 py-1 rounded-xl bg-gradient-to-r from-[#E76A4D] to-[#F5A623] text-white font-extrabold text-xs shadow-md hover:brightness-110 disabled:opacity-50 transition-all flex items-center gap-1.5"
      >
        <Play class="w-3.5 h-3.5 fill-white" />
        <span>{{ isRunning ? 'Running...' : 'Run Code' }}</span>
      </button>
    </div>

    <!-- Code Block -->
    <div class="p-3.5 bg-slate-950 font-mono text-xs text-slate-200 border-b border-white/5">
      <textarea
        v-model="editableCode"
        rows="5"
        class="w-full bg-transparent resize-y focus:outline-none text-emerald-300 leading-relaxed font-mono"
        spellcheck="false"
      />
    </div>

    <!-- Live Execution Results -->
    <div v-if="hasRun" class="p-3.5 bg-slate-900/90 font-mono text-xs">
      <div class="flex items-center justify-between text-[11px] text-slate-400 mb-2 border-b border-white/10 pb-1">
        <span>Console Log Output:</span>
        <span class="text-emerald-400 font-bold font-mono">{{ runtimeMs }}ms</span>
      </div>

      <div class="space-y-1">
        <div v-for="log in logs" :key="log.id" class="text-slate-200 flex items-start gap-2">
          <span class="text-[#E76A4D] font-bold">›</span>
          <span>{{ log.args.join(' ') }}</span>
        </div>

        <div v-if="returnValue !== undefined && returnValue !== 'undefined'" class="text-cyan-400 font-bold pt-1">
          Return: {{ returnValue }}
        </div>

        <div v-if="error" class="text-rose-400 font-bold pt-1">
          Error: {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Sparkles, Play } from 'lucide-vue-next'
import { executeJSCode, type LogEntry } from '~/utils/worker-runner'

const props = defineProps<{
  code?: string
  title?: string
}>()

const editableCode = ref(props.code || `function demo() {\n  const message = "Hello from MDC Playground!";\n  console.log(message);\n  return 42;\n}\ndemo();`)

const isRunning = ref(false)
const hasRun = ref(false)
const logs = ref<LogEntry[]>([])
const returnValue = ref<any>(undefined)
const error = ref<string | undefined>(undefined)
const runtimeMs = ref(0)

async function runInlineCode() {
  isRunning.value = true
  hasRun.value = true
  const res = await executeJSCode(editableCode.value)
  logs.value = res.logs
  returnValue.value = res.returnValue
  error.value = res.error
  runtimeMs.value = res.runtimeMs
  isRunning.value = false
}
</script>
