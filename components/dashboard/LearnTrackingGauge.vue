<template>
  <AppCard custom-class="h-full flex flex-col justify-between">
    <div class="flex items-center justify-between mb-2">
      <h3 class="text-base font-extrabold text-slate-900">Learn tracking</h3>
      <button class="text-slate-400 hover:text-slate-600">
        <MoreVertical class="w-4 h-4" />
      </button>
    </div>

    <!-- Multi-ring Circular Gauge -->
    <div class="flex items-center justify-center my-4 relative">
      <div class="w-36 h-36 rounded-full border-8 border-slate-100 flex items-center justify-center relative">
        <!-- SVG Concentric Donut Rings -->
        <svg class="w-36 h-36 -rotate-90 absolute inset-0" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="40" fill="none" stroke="#FFF0EB" stroke-width="8" />
          <circle
            cx="50" cy="50" r="40" fill="none"
            stroke="#E76A4D" stroke-width="8"
            stroke-dasharray="251.2"
            stroke-dashoffset="190"
            stroke-linecap="round"
          />
          <circle
            cx="50" cy="50" r="30" fill="none"
            stroke="#F5A623" stroke-width="6"
            stroke-dasharray="188.4"
            stroke-dashoffset="120"
            stroke-linecap="round"
          />
        </svg>

        <div class="text-center font-sans z-10">
          <span class="text-2xl font-extrabold text-slate-900 block font-mono">16%</span>
          <span class="text-[10px] text-slate-400 font-medium">Goal Distance</span>
        </div>
      </div>
    </div>

    <!-- Ring Legend -->
    <div class="flex items-center justify-center gap-4 text-xs font-semibold text-slate-600 pt-3 border-t border-[#F2D8D2]/60">
      <div class="flex items-center gap-1.5">
        <span class="w-2.5 h-2.5 rounded-full bg-[#E76A4D]" />
        <span>Month</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-2.5 h-2.5 rounded-full bg-[#F5A623]" />
        <span>Week</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-2.5 h-2.5 rounded-full bg-rose-400" />
        <span>Day</span>
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { MoreVertical } from 'lucide-vue-next'
import AppCard from '~/components/ui/AppCard.vue'
</script>
