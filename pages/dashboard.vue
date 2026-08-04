<template>
  <AppShell @open-command-palette="isCmdPaletteOpen = true">
    <CommandPalette :is-open="isCmdPaletteOpen" @close="isCmdPaletteOpen = false" @open="isCmdPaletteOpen = true" />

    <!-- Welcome Banner Header -->
    <div class="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
      <div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
          <span>Welcome Back</span>
          <span class="text-2xl">👋</span>
        </h1>
        <p class="text-xs sm:text-sm text-slate-500 font-medium mt-0.5">
          Let's learn something new today!
        </p>
      </div>

      <div class="flex items-center gap-2">
        <span class="px-3 py-1 rounded-full bg-[#E76A4D]/10 text-[#E76A4D] font-bold text-xs font-mono">
          PRO DASHBOARD
        </span>
      </div>
    </div>

    <!-- Main Dashboard Bento Grid (Matches Reference Image Layout) -->
    <div class="space-y-6">
      <!-- Top Row Grid (3/4 + 1/4) -->
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">

        <!-- Continue Learning Card -->
        <div class="lg:col-span-2">
          <ContinueLearningCard />
        </div>

        <!-- Progress Stats Card -->
        <AppCard custom-class="flex flex-col justify-between">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-xs font-bold text-slate-500 uppercase tracking-wider font-mono">Progress</h3>
            <select class="bg-[#FFF7F4] border border-[#F2D8D2] rounded-xl px-2 py-0.5 text-[11px] font-semibold text-slate-700">
              <option>Month ∨</option>
            </select>
          </div>

          <div class="space-y-3 my-2">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full bg-rose-500/10 flex items-center justify-center text-rose-500">
                <Clock class="w-4 h-4" />
              </div>
              <div>
                <span class="text-xs font-extrabold text-slate-900 block">40 hours</span>
                <span class="text-[10px] text-slate-400 font-medium">Time spend</span>
              </div>
            </div>

            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full bg-amber-500/10 flex items-center justify-center text-amber-500">
                <CheckCircle2 class="w-4 h-4" />
              </div>
              <div>
                <span class="text-xs font-extrabold text-slate-900 block">1 course</span>
                <span class="text-[10px] text-slate-400 font-medium">Completed</span>
              </div>
            </div>

            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full bg-[#E76A4D]/10 flex items-center justify-center text-[#E76A4D]">
                <BookOpen class="w-4 h-4" />
              </div>
              <div>
                <span class="text-xs font-extrabold text-slate-900 block">02 course</span>
                <span class="text-[10px] text-slate-400 font-medium">Enrolled</span>
              </div>
            </div>
          </div>
        </AppCard>

        <!-- Your Activity Matrix Card -->
        <ActivityDotMatrix />
      </div>

      <!-- Second Row Grid (Study Stats + Learn Tracking + Mentors + Motivation Banner) -->
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <!-- Study Statistics Bar Chart (2 Cols) -->
        <div class="lg:col-span-2">
          <StudyStatisticsChart />
        </div>

        <!-- Learn Tracking Circular Ring -->
        <LearnTrackingGauge />

        <!-- Motivation Banner Right Column -->
        <div class="md:row-span-2 lg:row-span-1">
          <MotivationBannerCard />
        </div>
      </div>

      <!-- Third Row Grid (Top Mentors + Daily JS Challenge) -->
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <!-- Top Mentors Card -->
        <div class="lg:col-span-2">
          <TopMentorsCard />
        </div>

        <!-- Daily JS Challenge Card (2 Cols) -->
        <div class="lg:col-span-2">
          <AppCard custom-class="h-full flex flex-col justify-between border-[#E76A4D]/40">
            <div>
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                  <div class="w-8 h-8 rounded-xl bg-[#E76A4D]/10 border border-[#E76A4D]/20 flex items-center justify-center text-[#E76A4D]">
                    <Target class="w-4 h-4" />
                  </div>
                  <div>
                    <h3 class="text-base font-extrabold text-slate-900 leading-tight">Daily JS Challenge</h3>
                    <p class="text-[11px] text-slate-400 font-medium">Array Flattening • +75 XP</p>
                  </div>
                </div>

                <button
                  @click="runDailyChallenge"
                  :disabled="isChallengeRunning"
                  class="px-4 py-2 rounded-[18px] bg-[#E76A4D] hover:bg-[#D85D3E] text-white font-extrabold text-xs shadow-md shadow-[#E76A4D]/20 transition-all flex items-center gap-1.5"
                >
                  <Play class="w-3.5 h-3.5 fill-white" />
                  <span>{{ isChallengeRunning ? 'Testing...' : 'Submit Challenge' }}</span>
                </button>
              </div>

              <!-- Challenge Code Editor -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-4">
                <div class="bg-slate-900 p-3 rounded-2xl border border-slate-800 font-mono text-xs text-emerald-300">
                  <textarea
                    v-model="dailyChallengeCode"
                    rows="5"
                    class="w-full bg-transparent text-emerald-300 focus:outline-none resize-none leading-relaxed"
                    spellcheck="false"
                  />
                </div>

                <div class="bg-[#FFF7F4] p-3 rounded-2xl border border-[#F2D8D2] font-mono text-xs flex flex-col justify-between">
                  <div>
                    <span class="text-[10px] text-slate-400 uppercase font-bold block mb-1">Status Output:</span>
                    <div v-if="challengeResult" class="space-y-1">
                      <div
                        :class="[
                          'p-2 rounded-xl border text-xs font-bold flex items-center gap-2',
                          challengeResult.passed ? 'bg-emerald-50 border-emerald-300 text-emerald-700' : 'bg-rose-50 border-rose-300 text-rose-700'
                        ]"
                      >
                        <CheckCircle2 v-if="challengeResult.passed" class="w-4 h-4 text-emerald-600" />
                        <AlertTriangle v-else class="w-4 h-4 text-rose-600" />
                        <span>{{ challengeResult.message }}</span>
                      </div>
                    </div>
                    <div v-else class="text-slate-500 italic py-3 text-center text-[11px]">
                      Run test specs against Web Worker evaluator.
                    </div>
                  </div>

                  <span class="text-[10px] text-slate-400 border-t border-[#F2D8D2] pt-2">
                    Test: <code class="text-slate-700">flattenArray([1, [2]]) =&gt; [1, 2]</code>
                  </span>
                </div>
              </div>
            </div>
          </AppCard>
        </div>
      </div>
    </div>
  </AppShell>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Clock, CheckCircle2, BookOpen, Target, Play, AlertTriangle } from 'lucide-vue-next'
import AppShell from '~/components/layout/AppShell.vue'
import CommandPalette from '~/components/ui/CommandPalette.vue'
import AppCard from '~/components/ui/AppCard.vue'
import ContinueLearningCard from '~/components/dashboard/ContinueLearningCard.vue'
import StudyStatisticsChart from '~/components/dashboard/StudyStatisticsChart.vue'
import LearnTrackingGauge from '~/components/dashboard/LearnTrackingGauge.vue'
import ActivityDotMatrix from '~/components/dashboard/ActivityDotMatrix.vue'
import TopMentorsCard from '~/components/dashboard/TopMentorsCard.vue'
import MotivationBannerCard from '~/components/dashboard/MotivationBannerCard.vue'
import { useProgressStore } from '~/stores/progress'
import { executeJSCode } from '~/utils/worker-runner'

definePageMeta({
  middleware: 'auth'
})

const isCmdPaletteOpen = ref(false)
const progressStore = useProgressStore()

const dailyChallengeCode = ref(`function flattenArray(arr) {
  return arr.reduce((acc, val) =>
    Array.isArray(val) ? acc.concat(flattenArray(val)) : acc.concat(val), []
  );
}`)

const isChallengeRunning = ref(false)
const challengeResult = ref<{ passed: boolean; message: string } | null>(null)

async function runDailyChallenge() {
  isChallengeRunning.value = true
  const res = await executeJSCode(dailyChallengeCode.value, [
    {
      id: 'dc-1',
      name: 'flattenArray flattens nested arrays',
      code: `
        const res = flattenArray([1, [2, [3, 4]], 5]);
        if (JSON.stringify(res) !== '[1,2,3,4,5]') {
          throw new Error('Expected [1,2,3,4,5] but got ' + JSON.stringify(res));
        }
      `
    }
  ])

  isChallengeRunning.value = false
  if (res.tests[0] && res.tests[0].passed) {
    challengeResult.value = {
      passed: true,
      message: 'Challenge Passed! +75 XP awarded.'
    }
    progressStore.totalXP += 75
  } else {
    challengeResult.value = {
      passed: false,
      message: res.tests[0]?.error || 'Assertion failed.'
    }
  }
}
</script>
