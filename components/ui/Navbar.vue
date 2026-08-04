<template>
  <header class="sticky top-0 z-40 w-full border-b border-white/10 bg-slate-950/80 backdrop-blur-xl">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <!-- Left: Logo & Links -->
      <div class="flex items-center gap-8">
        <NuxtLink to="/" class="flex items-center gap-2.5 group">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 via-cyan-500 to-indigo-500 p-0.5 shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
            <div class="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center font-mono font-extrabold text-emerald-400 text-sm">
              JS
            </div>
          </div>
          <div class="flex flex-col">
            <span class="font-bold text-base tracking-tight text-white group-hover:text-emerald-400 transition-colors">
              ScriptCraft
            </span>
            <span class="text-[10px] text-slate-400 font-mono -mt-1 tracking-wider uppercase">
              JS Masterclass
            </span>
          </div>
        </NuxtLink>

        <nav class="hidden md:flex items-center gap-1">
          <NuxtLink
            to="/dashboard"
            class="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
            :class="$route.path.startsWith('/dashboard') ? 'bg-white/10 text-white' : 'text-slate-400 hover:text-white hover:bg-white/5'"
          >
            Dashboard
          </NuxtLink>

          <NuxtLink
            to="/learn/01-foundations/01-closures"
            class="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
            :class="$route.path.startsWith('/learn') ? 'bg-white/10 text-white' : 'text-slate-400 hover:text-white hover:bg-white/5'"
          >
            Learn & IDE
          </NuxtLink>

          <NuxtLink
            to="/playground"
            class="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
            :class="$route.path.startsWith('/playground') ? 'bg-white/10 text-white' : 'text-slate-400 hover:text-white hover:bg-white/5'"
          >
            Playground
          </NuxtLink>
        </nav>
      </div>

      <!-- Right Actions -->
      <div class="flex items-center gap-3">
        <!-- Cmd+K Command Palette Trigger -->
        <button
          @click="$emit('open-command-palette')"
          class="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/90 border border-white/10 text-slate-400 hover:text-white hover:border-slate-700 text-xs transition-all"
        >
          <Search class="w-3.5 h-3.5" />
          <span>Search...</span>
          <kbd class="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px] font-mono text-slate-300">
            ⌘K
          </kbd>
        </button>

        <!-- Streak Counter -->
        <div class="flex items-center gap-1.5 px-3 py-1 bg-amber-500/10 border border-amber-500/20 rounded-full text-amber-400 text-xs font-semibold">
          <Flame class="w-4 h-4 fill-amber-500 text-amber-500 animate-pulse" />
          <span>{{ progressStore.streakDays }} Day Streak</span>
        </div>

        <!-- Total XP Badge -->
        <div class="hidden lg:flex items-center gap-1.5 px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-emerald-400 text-xs font-semibold">
          <Zap class="w-3.5 h-3.5 fill-emerald-400" />
          <span>{{ progressStore.totalXP }} XP</span>
        </div>

        <!-- Language Toggle -->
        <LanguageToggle />
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Flame, Zap, Search } from 'lucide-vue-next'
import LanguageToggle from './LanguageToggle.vue'
import { useProgressStore } from '~/stores/progress'

const progressStore = useProgressStore()

defineEmits(['open-command-palette'])
</script>
