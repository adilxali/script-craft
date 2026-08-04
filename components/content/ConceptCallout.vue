<template>
  <div
    :class="[
      'my-5 p-4 rounded-2xl border flex items-start gap-3.5 shadow-sm font-sans',
      type === 'hinglish'
        ? 'bg-amber-50/90 border-amber-300 text-amber-950'
        : type === 'tip'
        ? 'bg-emerald-50/90 border-emerald-300 text-emerald-950'
        : 'bg-[#FFF0EB] border-[#F2D8D2] text-slate-900'
    ]"
  >
    <div class="mt-0.5 shrink-0">
      <Globe v-if="type === 'hinglish'" class="w-5 h-5 text-amber-600" />
      <Lightbulb v-else-if="type === 'tip'" class="w-5 h-5 text-emerald-600" />
      <Info v-else class="w-5 h-5 text-[#E76A4D]" />
    </div>

    <div class="text-xs leading-relaxed space-y-1">
      <span
        class="font-extrabold uppercase tracking-wider text-[10px] block font-mono"
        :class="type === 'hinglish' ? 'text-amber-700' : type === 'tip' ? 'text-emerald-700' : 'text-[#E76A4D]'"
      >
        {{ title || (type === 'hinglish' ? 'Hinglish Concept Rule' : type === 'tip' ? 'Pro Tip' : 'Key Concept') }}
      </span>
      <div class="font-medium text-slate-800 text-xs sm:text-sm">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Globe, Lightbulb, Info } from 'lucide-vue-next'

defineProps<{
  type?: 'hinglish' | 'tip' | 'info'
  title?: string
}>()
</script>
