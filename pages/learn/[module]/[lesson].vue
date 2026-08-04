<template>
  <AppShell @open-command-palette="isCmdPaletteOpen = true">
    <CommandPalette :is-open="isCmdPaletteOpen" @close="isCmdPaletteOpen = false" @open="isCmdPaletteOpen = true" />

    <!-- Lesson Subheader Bar -->
    <div class="mb-4 p-3 bg-white border border-[#F2D8D2] rounded-2xl flex flex-wrap items-center justify-between gap-3 text-xs shadow-sm">
      <div class="flex items-center gap-3">
        <NuxtLink to="/dashboard" class="text-slate-500 hover:text-[#E76A4D] font-medium flex items-center gap-1 transition-colors">
          <ChevronLeft class="w-4 h-4" />
          <span>Dashboard</span>
        </NuxtLink>
        <span class="text-slate-300">/</span>
        <span class="text-slate-800 font-mono font-bold">
          Module {{ route.params.module }} › Lesson {{ route.params.lesson }}
        </span>
      </div>

      <div class="flex items-center gap-3">
        <button
          @click="markComplete"
          :disabled="isCompleted"
          :class="[
            'px-4 py-1.5 rounded-full font-bold text-xs transition-all flex items-center gap-1.5 shadow-sm',
            isCompleted
              ? 'bg-emerald-100 text-emerald-700 border border-emerald-300'
              : 'bg-[#E76A4D] hover:bg-[#D85D3E] text-white shadow-[#E76A4D]/20'
          ]"
        >
          <CheckCircle2 class="w-3.5 h-3.5" />
          <span>{{ isCompleted ? 'Completed (+50 XP)' : 'Mark Completed' }}</span>
        </button>

        <LanguageToggle />
      </div>
    </div>

    <!-- IDE Split-Pane View Container -->
    <div class="bg-white rounded-[24px] border border-[#F2D8D2] shadow-soft overflow-hidden h-[calc(100vh-12rem)] min-h-[500px]">
      <SplitPaneContainer>
        <!-- Left Pane: Content Reader -->
        <template #left>
          <div class="max-w-3xl mx-auto pb-12">
            <ContentDoc :path="contentPath" v-slot="{ doc }">
              <article class="prose prose-soft max-w-none">
                <ContentRenderer :value="doc" />
              </article>
            </ContentDoc>
          </div>
        </template>

        <!-- Right Pane: Monaco IDE + Console + Test Runner -->
        <template #right>
          <div class="h-full flex flex-col gap-2 p-1">
            <!-- Tabs -->
            <div class="flex items-center justify-between p-1.5 bg-[#FFF7F4] rounded-2xl border border-[#F2D8D2] shrink-0">
              <div class="flex items-center gap-1">
                <button
                  @click="activeTab = 'editor'"
                  :class="[
                    'px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5',
                    activeTab === 'editor' ? 'bg-white text-[#E76A4D] shadow-sm' : 'text-slate-500 hover:text-slate-800'
                  ]"
                >
                  <Code2 class="w-3.5 h-3.5" />
                  <span>Editor</span>
                </button>

                <button
                  @click="activeTab = 'tests'"
                  :class="[
                    'px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5',
                    activeTab === 'tests' ? 'bg-white text-[#E76A4D] shadow-sm' : 'text-slate-500 hover:text-slate-800'
                  ]"
                >
                  <CheckSquare class="w-3.5 h-3.5" />
                  <span>Tests ({{ testSpecs.length }})</span>
                </button>

                <button
                  @click="activeTab = 'console'"
                  :class="[
                    'px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5',
                    activeTab === 'console' ? 'bg-white text-cyan-600 shadow-sm' : 'text-slate-500 hover:text-slate-800'
                  ]"
                >
                  <Terminal class="w-3.5 h-3.5" />
                  <span>Console</span>
                </button>
              </div>

              <!-- Run Code Button -->
              <button
                @click="runCode"
                :disabled="isExecuting"
                class="px-4 py-1.5 rounded-xl bg-[#E76A4D] hover:bg-[#D85D3E] text-white font-extrabold text-xs shadow-md shadow-[#E76A4D]/20 transition-all flex items-center gap-1.5"
              >
                <Play class="w-3.5 h-3.5 fill-white" />
                <span>{{ isExecuting ? 'Running...' : 'Run Code (⌘↵)' }}</span>
              </button>
            </div>

            <!-- Tab Content -->
            <div class="flex-1 relative overflow-hidden flex flex-col gap-2">
              <div v-show="activeTab === 'editor'" class="h-3/5">
                <MonacoEditor
                  v-model="editorCode"
                  filename="solution.js"
                  @reset="resetCode"
                  @run="runCode"
                />
              </div>

              <div v-show="activeTab === 'tests'" class="h-3/5">
                <TestRunnerPanel
                  :tests="testResults"
                  :is-running="isExecuting"
                  @run-tests="runCode"
                />
              </div>

              <div :class="activeTab === 'console' ? 'h-full' : 'h-2/5'">
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
        </template>
      </SplitPaneContainer>
    </div>
  </AppShell>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ChevronLeft, CheckCircle2, Code2, CheckSquare, Terminal, Play } from 'lucide-vue-next'
import AppShell from '~/components/layout/AppShell.vue'
import CommandPalette from '~/components/ui/CommandPalette.vue'
import LanguageToggle from '~/components/ui/LanguageToggle.vue'
import SplitPaneContainer from '~/components/ide/SplitPaneContainer.vue'
import MonacoEditor from '~/components/ide/MonacoEditor.client.vue'
import ConsolePanel from '~/components/ide/ConsolePanel.vue'
import TestRunnerPanel from '~/components/ide/TestRunnerPanel.vue'
import { useLanguageStore } from '~/stores/language'
import { useProgressStore } from '~/stores/progress'
import { executeJSCode, type LogEntry, type TestResult, type TestSpec } from '~/utils/worker-runner'

definePageMeta({
  middleware: 'auth'
})

const route = useRoute()
const languageStore = useLanguageStore()
const progressStore = useProgressStore()

const isCmdPaletteOpen = ref(false)
const activeTab = ref<'editor' | 'tests' | 'console'>('editor')

const lessonKey = computed(() => `${route.params.module}/${route.params.lesson}`)

const contentPath = computed(() => {
  const lang = languageStore.currentLang
  return `/lessons/${route.params.module}/${route.params.lesson}.${lang}`
})

const isCompleted = computed(() => progressStore.isLessonCompleted(lessonKey.value))

const starterCode = ref(`function createCounter() {
  let count = 0;
  return function() {
    count++;
    return count;
  };
}

const counter = createCounter();
console.log("First call:", counter());
console.log("Second call:", counter());
`)

const editorCode = ref(starterCode.value)

const testSpecs = ref<TestSpec[]>([
  {
    id: 'test-1',
    name: 'createCounter returns a function that increments count',
    code: `
      const c = createCounter();
      if (c() !== 1) throw new Error("First invocation must return 1");
      if (c() !== 2) throw new Error("Second invocation must return 2");
    `
  },
  {
    id: 'test-2',
    name: 'Multiple counter instances maintain independent state',
    code: `
      const c1 = createCounter();
      const c2 = createCounter();
      c1(); c1();
      if (c1() !== 3) throw new Error("Counter 1 state should be 3");
      if (c2() !== 1) throw new Error("Counter 2 state was mutated!");
    `
  }
])

const isExecuting = ref(false)
const logs = ref<LogEntry[]>([])
const returnValue = ref<any>(undefined)
const runtimeMs = ref(0)
const executionStatus = ref<'idle' | 'running' | 'completed' | 'error'>('idle')
const executionError = ref<string | undefined>(undefined)
const testResults = ref<TestResult[]>([])

async function runCode() {
  isExecuting.value = true
  executionStatus.value = 'running'
  executionError.value = undefined

  const res = await executeJSCode(editorCode.value, testSpecs.value)

  logs.value = res.logs
  returnValue.value = res.returnValue
  runtimeMs.value = res.runtimeMs
  testResults.value = res.tests
  executionError.value = res.error

  isExecuting.value = false
  if (res.error) {
    executionStatus.value = 'error'
  } else {
    executionStatus.value = 'completed'
  }
}

function resetCode() {
  editorCode.value = starterCode.value
  logs.value = []
  returnValue.value = undefined
  executionStatus.value = 'idle'
  executionError.value = undefined
}

function markComplete() {
  progressStore.completeLesson(lessonKey.value, 50)
}

onMounted(() => {
  languageStore.initLanguage()
})
</script>
