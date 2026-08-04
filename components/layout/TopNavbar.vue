<template>
  <header class="w-full h-16 px-6 bg-white/70 backdrop-blur-xl border-b border-[#F2D8D2]/60 flex items-center justify-between sticky top-0 z-20 font-sans">
    <!-- Left: Search input -->
    <div class="flex items-center gap-4 flex-1 max-w-md">
      <div class="relative w-full">
        <Search class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          placeholder="Search lessons, topics, or code snippets..."
          @click="$emit('open-command-palette')"
          class="w-full bg-[#FFF7F4] border border-[#F2D8D2] rounded-2xl pl-10 pr-12 py-2 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-[#E76A4D] transition-colors cursor-pointer"
          readonly
        />
        <kbd class="absolute right-3 top-1/2 -translate-y-1/2 px-1.5 py-0.5 rounded bg-white border border-[#F2D8D2] text-[10px] font-mono text-slate-400">
          ⌘K
        </kbd>
      </div>
    </div>

    <!-- Right Actions -->
    <div class="flex items-center gap-4">
      <!-- Streak Flame -->
      <div class="flex items-center gap-1.5 px-3.5 py-1.5 bg-amber-500/10 border border-amber-500/20 rounded-full text-amber-600 text-xs font-bold shadow-sm">
        <Flame class="w-4 h-4 fill-amber-500 text-amber-500 animate-pulse" />
        <span>{{ progressStore.streakDays }} Days Streak</span>
      </div>

      <!-- XP Points Badge -->
      <div class="flex items-center gap-1.5 px-3.5 py-1.5 bg-[#E76A4D]/10 border border-[#E76A4D]/20 rounded-full text-[#E76A4D] text-xs font-bold shadow-sm">
        <Zap class="w-3.5 h-3.5 fill-[#E76A4D]" />
        <span>{{ progressStore.totalXP }} XP</span>
      </div>

      <!-- Language Toggle -->
      <LanguageToggle />

      <!-- Notification Bell Button -->
      <button class="relative p-2 rounded-2xl bg-white border border-[#F2D8D2] text-slate-600 hover:text-[#E76A4D] hover:border-[#E76A4D]/40 transition-colors shadow-sm">
        <Bell class="w-4 h-4" />
        <span class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-[#E76A4D]" />
      </button>

      <!-- User Profile Dropdown Avatar -->
      <NuxtLink to="/auth/login" class="flex items-center gap-2 pl-2 border-l border-[#F2D8D2]">
        <img
          :src="authStore.user?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80'"
          :alt="authStore.user?.name || 'User'"
          class="w-8 h-8 rounded-full object-cover border border-[#E76A4D]"
        />
      </NuxtLink>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Search, Flame, Zap, Bell } from 'lucide-vue-next'
import LanguageToggle from '~/components/ui/LanguageToggle.vue'
import { useProgressStore } from '~/stores/progress'
import { useAuthStore } from '~/stores/auth'

const progressStore = useProgressStore()
const authStore = useAuthStore()

defineEmits(['open-command-palette'])
</script>
