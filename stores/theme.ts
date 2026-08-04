import { defineStore } from 'pinia'
import { ref } from 'vue'

export type EditorTheme = 'vs-dark' | 'tokyo-night' | 'catppuccin'

export const useThemeStore = defineStore('theme', () => {
  const currentEditorTheme = ref<EditorTheme>('vs-dark')

  const themeOptions = [
    { id: 'vs-dark', name: 'VS Code Dark', bg: '#1e1e1e' },
    { id: 'tokyo-night', name: 'Tokyo Night', bg: '#1a1b26' },
    { id: 'catppuccin', name: 'Catppuccin Mocha', bg: '#1e1e2e' }
  ]

  function setEditorTheme(theme: EditorTheme) {
    currentEditorTheme.value = theme
    if (import.meta.client) {
      localStorage.setItem('scriptcraft_editor_theme', theme)
    }
  }

  function initTheme() {
    if (import.meta.client) {
      const saved = localStorage.getItem('scriptcraft_editor_theme') as EditorTheme
      if (saved && ['vs-dark', 'tokyo-night', 'catppuccin'].includes(saved)) {
        currentEditorTheme.value = saved
      }
    }
  }

  return {
    currentEditorTheme,
    themeOptions,
    setEditorTheme,
    initTheme
  }
})
