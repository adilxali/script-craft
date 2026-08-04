<template>
  <div class="my-6 p-5 rounded-2xl border border-[#F2D8D2] bg-[#FFF7F4] shadow-md font-sans">
    <div class="flex items-center gap-2 mb-3">
      <HelpCircle class="w-5 h-5 text-[#E76A4D]" />
      <span class="text-xs font-bold text-[#E76A4D] uppercase tracking-wider font-mono">Concept Check Quiz</span>
    </div>

    <h4 class="text-base font-extrabold text-slate-900 mb-4 leading-snug">
      {{ question }}
    </h4>

    <!-- Options List -->
    <div class="space-y-2.5 mb-4">
      <button
        v-for="(option, idx) in parsedOptions"
        :key="idx"
        @click="selectOption(idx)"
        :disabled="isSubmitted"
        :class="[
          'w-full p-3.5 rounded-2xl border text-left text-xs sm:text-sm font-semibold transition-all flex items-center justify-between',
          selectedIndex === idx
            ? isCorrect
              ? 'bg-emerald-100 border-emerald-400 text-emerald-950'
              : 'bg-rose-100 border-rose-400 text-rose-950'
            : isSubmitted && idx === correctIndex
            ? 'bg-emerald-50 border-emerald-300 text-emerald-900'
            : 'bg-white border-[#F2D8D2] hover:border-[#E76A4D]/50 text-slate-800 shadow-sm'
        ]"
      >
        <span>{{ option }}</span>
        <CheckCircle2 v-if="isSubmitted && idx === correctIndex" class="w-4.5 h-4.5 text-emerald-600" />
        <XCircle v-else-if="isSubmitted && selectedIndex === idx && !isCorrect" class="w-4.5 h-4.5 text-rose-600" />
      </button>
    </div>

    <!-- Explanation Box -->
    <div v-if="isSubmitted" class="p-4 rounded-2xl bg-white border border-[#F2D8D2] text-xs leading-relaxed space-y-2">
      <div class="flex items-center gap-2 font-bold" :class="isCorrect ? 'text-emerald-700' : 'text-rose-700'">
        <Award v-if="isCorrect" class="w-4 h-4" />
        <AlertCircle v-else class="w-4 h-4" />
        <span>{{ isCorrect ? 'Sahi Jawab! (+25 XP)' : 'Galat Jawab! Check explanation below.' }}</span>
      </div>

      <p class="text-slate-700 font-medium">
        {{ explanation }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { HelpCircle, CheckCircle2, XCircle, Award, AlertCircle } from 'lucide-vue-next'
import { useProgressStore } from '~/stores/progress'
import { useSound } from '~/composables/useSound'

const props = defineProps<{
  question: string
  options: string | string[]
  answer: number
  explanation: string
}>()

const progressStore = useProgressStore()
const { playSuccessSound, playErrorSound } = useSound()

const selectedIndex = ref<number | null>(null)
const isSubmitted = ref(false)

const parsedOptions = computed(() => {
  if (Array.isArray(props.options)) return props.options
  try {
    return JSON.parse(props.options)
  } catch (e) {
    return props.options.split('|')
  }
})

const correctIndex = computed(() => Number(props.answer))
const isCorrect = computed(() => selectedIndex.value === correctIndex.value)

function selectOption(idx: number) {
  if (isSubmitted.value) return
  selectedIndex.value = idx
  isSubmitted.value = true

  if (idx === correctIndex.value) {
    progressStore.totalXP += 25
    playSuccessSound()
  } else {
    playErrorSound()
  }
}
</script>
