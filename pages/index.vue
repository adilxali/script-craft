<template>
  <div class="min-h-screen bg-[#FFF7F4] text-slate-800 selection:bg-[#E76A4D] selection:text-white relative overflow-hidden font-sans">
    <CommandPalette :is-open="isCmdPaletteOpen" @close="isCmdPaletteOpen = false" @open="isCmdPaletteOpen = true" />

    <!-- Ambient Peach Radial Highlights -->
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[400px] bg-gradient-to-b from-[#E76A4D]/20 via-[#F08C6A]/10 to-transparent blur-[120px] pointer-events-none rounded-full" />

    <!-- Top Header -->
    <header class="w-full max-w-7xl mx-auto px-6 h-20 flex items-center justify-between relative z-10">
      <NuxtLink to="/" class="flex items-center gap-3 group">
        <div class="w-10 h-10 rounded-2xl bg-[#E76A4D] flex items-center justify-center text-white shadow-md shadow-[#E76A4D]/30 group-hover:scale-105 transition-transform">
          <Play class="w-5 h-5 fill-white ml-0.5" />
        </div>
        <span class="font-black text-xl text-slate-900 tracking-tight">ScriptCraft</span>
      </NuxtLink>

      <div class="flex items-center gap-4">
        <LanguageToggle />
        <NuxtLink
          to="/dashboard"
          class="px-5 py-2.5 rounded-[18px] bg-[#E76A4D] hover:bg-[#D85D3E] text-white font-extrabold text-xs shadow-md shadow-[#E76A4D]/20 transition-all"
        >
          Student Dashboard →
        </NuxtLink>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="pt-16 pb-12 px-4 sm:px-6 max-w-5xl mx-auto text-center relative z-10">
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white border border-[#F2D8D2] text-[#E76A4D] text-xs font-bold shadow-sm mb-6">
        <Sparkles class="w-4 h-4 text-[#E76A4D]" />
        <span>Next-Gen Interactive JS Platform • English + Hinglish</span>
      </div>

      <h1 class="text-4xl sm:text-6xl font-black text-slate-900 tracking-tight leading-[1.15] max-w-4xl mx-auto">
        Learn Modern JavaScript with
        <span class="bg-gradient-to-r from-[#E76A4D] via-[#F08C6A] to-[#F5A623] bg-clip-text text-transparent">
          Real-Time IDE Feedback
        </span>
      </h1>

      <p class="mt-6 text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
        Master closures, async promises, prototypal inheritance, and ES6+ patterns through in-browser Web Worker code execution and interactive Hinglish explanations.
      </p>

      <div class="mt-8 flex flex-wrap items-center justify-center gap-4">
        <NuxtLink
          to="/dashboard"
          class="px-8 py-3.5 rounded-[18px] bg-[#E76A4D] hover:bg-[#D85D3E] text-white font-extrabold text-sm shadow-xl shadow-[#E76A4D]/25 hover:-translate-y-0.5 transition-all flex items-center gap-2"
        >
          <Rocket class="w-4 h-4 fill-white" />
          <span>Launch Dashboard</span>
        </NuxtLink>

        <NuxtLink
          to="/playground"
          class="px-8 py-3.5 rounded-[18px] bg-white border border-[#F2D8D2] hover:bg-[#FFF7F4] text-slate-800 font-extrabold text-sm shadow-sm transition-all flex items-center gap-2"
        >
          <Code2 class="w-4 h-4 text-[#E76A4D]" />
          <span>Open Playground</span>
        </NuxtLink>
      </div>
    </section>

    <!-- Bento Grid Showcase -->
    <section class="py-12 px-4 sm:px-6 max-w-6xl mx-auto relative z-10">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <AppCard hoverable custom-class="md:col-span-2">
          <div class="w-10 h-10 rounded-2xl bg-[#E76A4D]/10 flex items-center justify-center text-[#E76A4D] mb-4">
            <Globe class="w-5 h-5" />
          </div>
          <h3 class="text-lg font-extrabold text-slate-900">Dual Language Engine (EN + Hinglish)</h3>
          <p class="text-xs text-slate-500 mt-2 leading-relaxed">
            Switch between technical English and Roman Hindi explanations seamlessly during your lessons.
          </p>
        </AppCard>

        <AppCard hoverable>
          <div class="w-10 h-10 rounded-2xl bg-[#F5A623]/10 flex items-center justify-center text-[#F5A623] mb-4">
            <Cpu class="w-5 h-5" />
          </div>
          <h3 class="text-lg font-extrabold text-slate-900">Web Worker Engine</h3>
          <p class="text-xs text-slate-500 mt-2 leading-relaxed">
            Zero-latency, safely isolated JS execution capturing logs and runtime timing.
          </p>
        </AppCard>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Play, Sparkles, Rocket, Code2, Globe, Cpu } from 'lucide-vue-next'
import CommandPalette from '~/components/ui/CommandPalette.vue'
import LanguageToggle from '~/components/ui/LanguageToggle.vue'
import AppCard from '~/components/ui/AppCard.vue'

const isCmdPaletteOpen = ref(false)
</script>
