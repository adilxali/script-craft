<template>
  <AppCard custom-class="h-full flex flex-col justify-between">
    <div class="flex items-center justify-between mb-2">
      <h3 class="text-xs font-bold text-slate-500 uppercase tracking-wider font-mono">Your Activity</h3>
    </div>

    <div class="my-2">
      <div class="text-3xl font-black text-slate-900 font-mono flex items-baseline gap-2">
        <span>17</span>
        <span class="text-xs font-sans font-semibold text-slate-500">Days</span>
      </div>
      <p class="text-[11px] font-semibold text-slate-400 mt-0.5">68 hours 20 minutes</p>
    </div>

    <!-- Dot Matrix Grid -->
    <div class="grid grid-cols-8 gap-2 my-3">
      <div
        v-for="i in 24"
        :key="i"
        :class="[
          'w-3.5 h-3.5 rounded-full transition-all',
          i <= 17 ? 'bg-amber-400 shadow-sm shadow-amber-400/30' : 'bg-slate-100 border border-slate-200'
        ]"
      />
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import AppCard from '~/components/ui/AppCard.vue'
</script>
