import { defineStore } from 'pinia'
import { ref } from 'vue'

export type SupportedLanguage = 'en' | 'hi'

export const useLanguageStore = defineStore('language', () => {
  const currentLang = ref<SupportedLanguage>('en')

  function setLanguage(lang: SupportedLanguage) {
    currentLang.value = lang
    if (import.meta.client) {
      localStorage.setItem('scriptcraft_lang', lang)
    }
  }

  function toggleLanguage() {
    setLanguage(currentLang.value === 'en' ? 'hi' : 'en')
  }

  function initLanguage() {
    if (import.meta.client) {
      const saved = localStorage.getItem('scriptcraft_lang') as SupportedLanguage
      if (saved === 'en' || saved === 'hi') {
        currentLang.value = saved
      }
    }
  }

  return {
    currentLang,
    setLanguage,
    toggleLanguage,
    initLanguage
  }
})
