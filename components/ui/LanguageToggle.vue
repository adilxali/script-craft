<template>
  <div class="inline-flex items-center p-1 bg-slate-900/80 border border-white/10 rounded-full backdrop-blur-md">
    <button
      @click="languageStore.setLanguage('en')"
      :class="[
        'px-3 py-1 text-xs font-semibold rounded-full transition-all duration-200 flex items-center gap-1.5',
        languageStore.currentLang === 'en'
          ? 'bg-gradient-to-r from-emerald-500 to-cyan-500 text-slate-950 shadow-md shadow-emerald-500/20'
          : 'text-slate-400 hover:text-slate-200'
      ]"
    >
      <span class="text-[10px] uppercase tracking-wider font-bold">EN</span>
      <span>English</span>
    </button>

    <button
      @click="languageStore.setLanguage('hi')"
      :class="[
        'px-3 py-1 text-xs font-semibold rounded-full transition-all duration-200 flex items-center gap-1.5',
        languageStore.currentLang === 'hi'
          ? 'bg-gradient-to-r from-emerald-500 to-cyan-500 text-slate-950 shadow-md shadow-emerald-500/20'
          : 'text-slate-400 hover:text-slate-200'
      ]"
    >
      <span class="text-[10px] uppercase tracking-wider font-bold">HI</span>
      <span>Hinglish</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { useLanguageStore } from '~/stores/language'

const languageStore = useLanguageStore()
</script>
