<template>
  <div class="w-full h-full flex flex-col bg-slate-950 border border-white/10 rounded-xl overflow-hidden font-mono text-xs shadow-inner">
    <!-- Header Toolbar -->
    <div class="px-4 py-2 bg-slate-900/90 border-b border-white/10 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="font-bold text-slate-300 flex items-center gap-1.5">
          <Terminal class="w-4 h-4 text-cyan-400" />
          <span>Console Output</span>
        </span>

        <!-- Status indicator -->
        <span
          v-if="status === 'running'"
          class="px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-[10px] flex items-center gap-1 animate-pulse"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-cyan-400" />
          <span>Executing...</span>
        </span>
        <span
          v-else-if="status === 'completed'"
          class="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] flex items-center gap-1"
        >
          <CheckCircle2 class="w-3 h-3 text-emerald-400" />
          <span>Finished in {{ runtimeMs }}ms</span>
        </span>
        <span
          v-else-if="status === 'error'"
          class="px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 text-[10px] flex items-center gap-1"
        >
          <AlertTriangle class="w-3 h-3 text-rose-400" />
          <span>Failed</span>
        </span>
      </div>

      <div class="flex items-center gap-2">
        <span v-if="logs.length > 0" class="text-[11px] text-slate-500">
          {{ logs.length }} {{ logs.length === 1 ? 'log' : 'logs' }}
        </span>

        <button
          @click="$emit('clear')"
          class="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition-colors"
          title="Clear Console"
        >
          <Trash2 class="w-3.5 h-3.5" />
        </button>
      </div>
    </div>

    <!-- Logs Container -->
    <div class="flex-1 overflow-y-auto p-3 space-y-2 max-h-[350px] min-h-[140px] bg-slate-950/70">
      <div v-if="logs.length === 0 && !returnValue && !error" class="h-full flex flex-col items-center justify-center text-slate-600 space-y-2 py-8">
        <Terminal class="w-8 h-8 opacity-40 text-slate-500" />
        <p class="text-xs font-sans">Console output will appear here after code execution.</p>
      </div>

      <!-- Log Entries -->
      <div
        v-for="log in logs"
        :key="log.id"
        :class="[
          'px-3 py-1.5 rounded border text-xs leading-relaxed flex items-start justify-between gap-3 font-mono transition-all',
          log.level === 'error'
            ? 'bg-rose-950/40 border-rose-500/30 text-rose-300'
            : log.level === 'warn'
            ? 'bg-amber-950/40 border-amber-500/30 text-amber-300'
            : 'bg-slate-900/60 border-white/5 text-slate-200'
        ]"
      >
        <div class="flex items-start gap-2 overflow-x-auto">
          <span class="text-slate-500 select-none">›</span>
          <div class="whitespace-pre-wrap break-all">
            <span v-for="(arg, i) in log.args" :key="i" class="mr-2">
              {{ arg }}
            </span>
          </div>
        </div>
        <span class="text-[10px] text-slate-500 shrink-0 select-none">
          {{ log.timestamp }}
        </span>
      </div>

      <!-- Return Value Section -->
      <div v-if="returnValue !== undefined && returnValue !== 'undefined'" class="mt-3 pt-2 border-t border-white/10">
        <div class="px-3 py-2 rounded bg-cyan-950/30 border border-cyan-500/20 text-cyan-300 flex items-start gap-2">
          <CornerDownRight class="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
          <div class="overflow-x-auto">
            <span class="text-[10px] text-cyan-400 uppercase font-bold block mb-0.5">Return Value</span>
            <span class="text-slate-100 font-mono font-semibold">{{ returnValue }}</span>
          </div>
        </div>
      </div>

      <!-- Runtime Exception -->
      <div v-if="error" class="mt-2 p-3 rounded bg-rose-950/50 border border-rose-500/40 text-rose-300">
        <div class="flex items-center gap-2 font-bold text-rose-400 mb-1">
          <AlertOctagon class="w-4 h-4" />
          <span>Runtime Error</span>
        </div>
        <p class="text-xs whitespace-pre-wrap font-mono">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Terminal, Trash2, CheckCircle2, AlertTriangle, CornerDownRight, AlertOctagon } from 'lucide-vue-next'
import type { LogEntry } from '~/utils/worker-runner'

defineProps<{
  logs: LogEntry[]
  returnValue?: any
  runtimeMs?: number
  status?: 'idle' | 'running' | 'completed' | 'error'
  error?: string
}>()

defineEmits(['clear'])
</script>
