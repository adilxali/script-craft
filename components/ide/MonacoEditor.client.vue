<template>
  <div class="w-full h-full flex flex-col bg-slate-950 border border-white/10 rounded-xl overflow-hidden shadow-inner">
    <!-- Editor Header Controls -->
    <div class="px-4 py-2 bg-slate-900/90 border-b border-white/10 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <div class="flex gap-1.5">
          <div class="w-2.5 h-2.5 rounded-full bg-rose-500/80" />
          <div class="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
          <div class="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
        </div>
        <span class="text-xs font-mono text-slate-400 ml-2 font-medium flex items-center gap-1.5">
          <Code2 class="w-3.5 h-3.5 text-emerald-400" />
          <span>{{ filename || 'index.js' }}</span>
        </span>
      </div>

      <div class="flex items-center gap-3">
        <!-- Theme Selector Dropdown -->
        <div class="flex items-center gap-1.5 text-xs text-slate-400">
          <Palette class="w-3.5 h-3.5 text-slate-400" />
          <select
            v-model="selectedTheme"
            class="bg-slate-800 border border-slate-700 text-slate-200 rounded px-2 py-0.5 text-xs focus:outline-none focus:border-emerald-500"
            @change="updateTheme"
          >
            <option value="vs-dark">VS Code Dark</option>
            <option value="tokyo-night">Tokyo Night</option>
            <option value="catppuccin">Catppuccin</option>
          </select>
        </div>

        <!-- Reset Button -->
        <button
          @click="$emit('reset')"
          class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-mono transition-colors flex items-center gap-1"
          title="Reset starter code"
        >
          <RotateCcw class="w-3 h-3 text-slate-400" />
          <span>Reset</span>
        </button>
      </div>
    </div>

    <!-- Monaco Editor Body -->
    <div class="flex-1 relative min-h-[300px]">
      <VueMonacoEditor
        v-model:value="codeValue"
        language="javascript"
        :theme="monacoTheme"
        :options="editorOptions"
        @mount="handleEditorMount"
        class="w-full h-full"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { VueMonacoEditor } from '@guolao/vue-monaco-editor'
import { Code2, Palette, RotateCcw } from 'lucide-vue-next'
import { useThemeStore } from '~/stores/theme'

const props = defineProps<{
  modelValue: string
  filename?: string
}>()

const emit = defineEmits(['update:modelValue', 'reset', 'run'])

const themeStore = useThemeStore()

const codeValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const selectedTheme = ref(themeStore.currentEditorTheme)

const monacoTheme = computed(() => {
  return selectedTheme.value === 'vs-dark' ? 'vs-dark' : 'vs-dark'
})

function updateTheme() {
  themeStore.setEditorTheme(selectedTheme.value)
}

const editorOptions = {
  automaticLayout: true,
  formatOnType: true,
  formatOnPaste: true,
  minimap: { enabled: false },
  fontSize: 13,
  fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
  lineHeight: 22,
  cursorBlinking: 'smooth',
  cursorSmoothCaretAnimation: 'on',
  smoothScrolling: true,
  padding: { top: 12, bottom: 12 },
  renderLineHighlight: 'all',
  scrollBeyondLastLine: false,
  tabSize: 2
}

function handleEditorMount(editor: any, monaco: any) {
  // Define custom Tokyo Night theme
  monaco.editor.defineTheme('tokyo-night', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'comment', foreground: '565f89', fontStyle: 'italic' },
      { token: 'keyword', foreground: 'bb9af7' },
      { token: 'string', foreground: '9ece6a' },
      { token: 'number', foreground: 'ff9e64' },
      { token: 'identifier', foreground: '7dcfff' }
    ],
    colors: {
      'editor.background': '#1a1b26',
      'editor.foreground': '#a9b1d6',
      'editor.lineHighlightBackground': '#24283b',
      'editorCursor.foreground': '#c0caf5'
    }
  })

  // Define custom Catppuccin theme
  monaco.editor.defineTheme('catppuccin', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'comment', foreground: '6c7086', fontStyle: 'italic' },
      { token: 'keyword', foreground: 'cba6f7' },
      { token: 'string', foreground: 'a6e3a1' },
      { token: 'number', foreground: 'fab387' },
      { token: 'identifier', foreground: '89dceb' }
    ],
    colors: {
      'editor.background': '#1e1e2e',
      'editor.foreground': '#cdd6f4',
      'editor.lineHighlightBackground': '#313244',
      'editorCursor.foreground': '#f5e0dc'
    }
  })

  // Add keyboard shortcut: Cmd+Enter or Ctrl+Enter to Run Code
  editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
    emit('run')
  })
}

watch(() => themeStore.currentEditorTheme, (newTheme) => {
  selectedTheme.value = newTheme
})
</script>
