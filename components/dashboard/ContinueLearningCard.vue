<template>
  <AppCard glow-color="coral" hoverable custom-class="flex flex-col justify-between h-full border-[#F2D8D2]">
    <div>
      <div class="flex items-center justify-between mb-3">
        <span class="px-3 py-1 rounded-full bg-[#E76A4D]/10 text-[#E76A4D] font-extrabold text-[11px] uppercase tracking-wider font-mono">
          ACTIVE MODULE
        </span>
        <span class="text-xs font-extrabold text-[#F5A623] flex items-center gap-1 font-mono">
          <span>⚡</span>
          <span>Module 1</span>
        </span>
      </div>

      <h3 class="text-xl font-extrabold text-slate-900 leading-snug mb-3">
        {{ title || 'Module 1: JS Foundations & Scope' }}
      </h3>

      <!-- Course Metadata Pills -->
      <div class="flex flex-wrap items-center gap-3 text-xs font-bold text-slate-600 mb-5">
        <span class="px-2.5 py-1 rounded-xl bg-rose-50 border border-rose-200/80 text-rose-600 flex items-center gap-1.5">
          <Clock class="w-3.5 h-3.5" />
          <span>1 hr 40 mnts</span>
        </span>
        <span class="px-2.5 py-1 rounded-xl bg-amber-50 border border-amber-200/80 text-amber-600 flex items-center gap-1.5">
          <BookOpen class="w-3.5 h-3.5" />
          <span>8 chapters</span>
        </span>
        <span class="px-2.5 py-1 rounded-xl bg-orange-50 border border-orange-200/80 text-orange-600 flex items-center gap-1.5">
          <PlayCircle class="w-3.5 h-3.5" />
          <span>7 videos</span>
        </span>
      </div>

      <!-- Course Progress Bar -->
      <div class="space-y-1.5 mb-6">
        <div class="flex items-center justify-between text-xs font-bold">
          <span class="text-slate-400">Course complete</span>
          <span class="text-[#E76A4D] font-mono font-extrabold">60%</span>
        </div>
        <div class="w-full bg-slate-100 h-3 rounded-full overflow-hidden border border-slate-200/70 p-0.5">
          <div class="bg-gradient-to-r from-[#E76A4D] via-[#F08C6A] to-[#F5A623] h-full w-[60%] rounded-full transition-all duration-500 shadow-sm" />
        </div>
      </div>
    </div>

    <!-- Continue Button -->
    <NuxtLink
      to="/learn/01-foundations/01-closures"
      class="w-full py-3.5 px-5 rounded-[18px] bg-gradient-to-r from-[#E76A4D] to-[#F08C6A] hover:brightness-105 text-white font-extrabold text-xs tracking-wide transition-all flex items-center justify-between shadow-md shadow-[#E76A4D]/25 group"
    >
      <span>Continue learning</span>
      <div class="w-7 h-7 rounded-full bg-white/20 flex items-center justify-center text-white group-hover:translate-x-1 transition-transform">
        <Play class="w-3.5 h-3.5 fill-white ml-0.5" />
      </div>
    </NuxtLink>
  </AppCard>
</template>

<script setup lang="ts">
import { Clock, BookOpen, PlayCircle, Play } from 'lucide-vue-next'
import AppCard from '~/components/ui/AppCard.vue'

defineProps<{ title?: string }>()
</script>
