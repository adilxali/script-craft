<template>
  <div class="w-full h-full flex flex-col bg-slate-950 border border-white/10 rounded-xl overflow-hidden shadow-inner">
    <!-- Header -->
    <div class="px-4 py-2.5 bg-slate-900/90 border-b border-white/10 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <CheckSquare class="w-4 h-4 text-emerald-400" />
        <span class="font-bold text-xs text-slate-200">Automated Test Suite</span>
      </div>

      <div class="flex items-center gap-3">
        <!-- Test summary count -->
        <span v-if="tests.length > 0" class="text-xs font-mono font-semibold">
          <span :class="allPassed ? 'text-emerald-400' : 'text-slate-400'">
            {{ passedCount }} / {{ tests.length }} Passed
          </span>
        </span>

        <button
          @click="$emit('run-tests')"
          :disabled="isRunning"
          class="px-3 py-1 rounded bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-slate-950 font-bold text-xs shadow-md shadow-emerald-500/20 transition-all flex items-center gap-1.5"
        >
          <Play class="w-3 h-3 fill-slate-950" />
          <span>{{ isRunning ? 'Testing...' : 'Run Tests' }}</span>
        </button>
      </div>
    </div>

    <!-- Test List -->
    <div class="flex-1 overflow-y-auto p-4 space-y-3 bg-slate-950/70">
      <div v-if="tests.length === 0" class="text-center py-6 text-slate-500 text-xs">
        No test specs attached to this lesson.
      </div>

      <div
        v-for="test in tests"
        :key="test.id"
        :class="[
          'p-3 rounded-lg border transition-all flex flex-col gap-2',
          test.passed === true
            ? 'bg-emerald-950/20 border-emerald-500/30'
            : test.passed === false
            ? 'bg-rose-950/30 border-rose-500/40'
            : 'bg-slate-900/50 border-white/5'
        ]"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <CheckCircle2 v-if="test.passed === true" class="w-4 h-4 text-emerald-400 shrink-0" />
            <XCircle v-else-if="test.passed === false" class="w-4 h-4 text-rose-400 shrink-0" />
            <Circle v-else class="w-4 h-4 text-slate-500 shrink-0" />
            <span class="text-xs font-medium text-slate-200">{{ test.name }}</span>
          </div>

          <!-- Status badge -->
          <span
            v-if="test.passed === true"
            class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
          >
            PASS
          </span>
          <span
            v-else-if="test.passed === false"
            class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-rose-500/20 text-rose-400 border border-rose-500/30"
          >
            FAIL
          </span>
          <span
            v-else
            class="px-2 py-0.5 rounded-full text-[10px] font-medium uppercase tracking-wider bg-slate-800 text-slate-400"
          >
            PENDING
          </span>
        </div>

        <!-- Failure breakdown -->
        <div v-if="test.passed === false && test.error" class="px-3 py-2 bg-rose-950/50 rounded border border-rose-500/20 text-[11px] font-mono text-rose-300">
          <span class="font-bold block mb-0.5 text-rose-400">Assertion Error:</span>
          {{ test.error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { CheckSquare, Play, CheckCircle2, XCircle, Circle } from 'lucide-vue-next'
import type { TestResult } from '~/utils/worker-runner'

const props = defineProps<{
  tests: TestResult[]
  isRunning?: boolean
}>()

defineEmits(['run-tests'])

const passedCount = computed(() => props.tests.filter(t => t.passed).length)
const allPassed = computed(() => props.tests.length > 0 && passedCount.value === props.tests.length)
</script>
