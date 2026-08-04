<template>
  <AppCard glow-color="amber" custom-class="h-full flex flex-col justify-between">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div>
        <h3 class="text-base font-extrabold text-slate-900">Study Statistics</h3>
        <p class="text-[11px] text-slate-400 font-medium">Weekly hours spent learning JS</p>
      </div>

      <select class="bg-[#FFF7F4] border border-[#F2D8D2] rounded-xl px-3 py-1 text-xs font-bold text-[#E76A4D] focus:outline-none cursor-pointer">
        <option value="weekly">Weekly ∨</option>
        <option value="monthly">Monthly ∨</option>
      </select>
    </div>

    <!-- Chart Bars Grid -->
    <div class="relative pt-6 pb-2">
      <!-- Y-Axis Lines -->
      <div class="space-y-4 text-[10px] font-mono text-slate-400 font-bold">
        <div class="flex items-center gap-2">
          <span class="w-4">8h</span>
          <div class="flex-1 border-b border-dashed border-slate-200" />
        </div>
        <div class="flex items-center gap-2">
          <span class="w-4">7h</span>
          <div class="flex-1 border-b border-dashed border-slate-200" />
        </div>
        <div class="flex items-center gap-2">
          <span class="w-4">5h</span>
          <div class="flex-1 border-b border-dashed border-slate-200" />
        </div>
        <div class="flex items-center gap-2">
          <span class="w-4">3h</span>
          <div class="flex-1 border-b border-dashed border-slate-200" />
        </div>
        <div class="flex items-center gap-2">
          <span class="w-4">1h</span>
          <div class="flex-1 border-b border-dashed border-slate-200" />
        </div>
        <div class="flex items-center gap-2">
          <span class="w-4">0h</span>
          <div class="flex-1 border-b border-slate-200" />
        </div>
      </div>

      <!-- Bars Container -->
      <div class="absolute inset-x-8 bottom-6 top-6 flex items-end justify-between px-2">
        <div v-for="bar in daysData" :key="bar.day" class="flex flex-col items-center gap-1.5 flex-1 group">
          <!-- Tooltip on Hover -->
          <div class="opacity-0 group-hover:opacity-100 transition-opacity text-[10px] font-mono font-bold text-[#E76A4D] bg-[#FFF0EB] px-1.5 py-0.5 rounded border border-[#F2D8D2] -mb-1">
            {{ bar.hours }}h
          </div>

          <!-- Bar Track -->
          <div class="w-7 bg-slate-100 rounded-t-xl h-36 relative flex items-end overflow-hidden border border-slate-200/60 p-0.5">
            <div
              class="w-full rounded-t-lg transition-all duration-500 bg-gradient-to-t from-[#E76A4D] via-[#F08C6A] to-[#F5A623] shadow-sm"
              :style="{ height: bar.height + '%' }"
            />
          </div>
          <span class="text-[11px] font-bold text-slate-500 group-hover:text-[#E76A4D] transition-colors">{{ bar.day }}</span>
        </div>
      </div>
    </div>

    <!-- Legend Footer -->
    <div class="flex items-center justify-between text-xs font-extrabold text-slate-600 pt-3 border-t border-[#F2D8D2]/60">
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-gradient-to-r from-[#E76A4D] to-[#F5A623]" />
          <span>Active Study</span>
        </div>
        <div class="flex items-center gap-1.5">
          <span class="w-3 h-3 rounded-full bg-slate-200" />
          <span>Goal Target</span>
        </div>
      </div>

      <span class="text-[#E76A4D] font-mono text-[11px]">Avg: 5.4h/day</span>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import AppCard from '~/components/ui/AppCard.vue'

const daysData = [
  { day: 'Sun', height: 35, hours: 2.8 },
  { day: 'Mon', height: 80, hours: 6.4 },
  { day: 'Tue', height: 60, hours: 4.8 },
  { day: 'Wed', height: 95, hours: 7.6 },
  { day: 'Thu', height: 75, hours: 6.0 },
  { day: 'Fri', height: 85, hours: 6.8 },
  { day: 'Sat', height: 40, hours: 3.2 }
]
</script>
