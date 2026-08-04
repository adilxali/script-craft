<template>
  <div
    ref="containerRef"
    class="w-full h-full flex flex-col md:flex-row overflow-hidden bg-white"
    @mousemove="onMouseMove"
    @mouseup="onMouseUp"
    @mouseleave="onMouseUp"
  >
    <!-- Left Pane: Content -->
    <div
      :style="{ width: isMobile ? '100%' : leftPaneWidth + '%' }"
      class="h-full overflow-y-auto border-r border-[#F2D8D2] p-4 sm:p-6 bg-white text-slate-900"
    >
      <slot name="left" />
    </div>

    <!-- Drag Divider Handle (Desktop) -->
    <div
      v-if="!isMobile"
      @mousedown="onMouseDown"
      class="w-2 hover:w-2 h-full bg-[#FFF7F4] border-x border-[#F2D8D2] hover:bg-[#E76A4D]/30 cursor-col-resize flex items-center justify-center transition-colors select-none group"
    >
      <div class="w-1 h-8 rounded-full bg-slate-300 group-hover:bg-[#E76A4D] transition-colors" />
    </div>

    <!-- Right Pane: IDE / Monaco + Console -->
    <div
      :style="{ width: isMobile ? '100%' : (100 - leftPaneWidth) + '%' }"
      class="h-full overflow-hidden flex flex-col p-2 sm:p-3 bg-[#FFF7F4]"
    >
      <slot name="right" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const leftPaneWidth = ref(48)
const isDragging = ref(false)
const containerRef = ref<HTMLElement | null>(null)
const isMobile = ref(false)

function checkMobile() {
  if (import.meta.client) {
    isMobile.value = window.innerWidth < 768
  }
}

function onMouseDown(e: MouseEvent) {
  e.preventDefault()
  isDragging.value = true
}

function onMouseMove(e: MouseEvent) {
  if (!isDragging.value || !containerRef.value) return
  const containerRect = containerRef.value.getBoundingClientRect()
  const offsetX = e.clientX - containerRect.left
  const percentage = (offsetX / containerRect.width) * 100

  if (percentage >= 25 && percentage <= 75) {
    leftPaneWidth.value = percentage
  }
}

function onMouseUp() {
  isDragging.value = false
}

onMounted(() => {
  checkMobile()
  if (import.meta.client) {
    window.addEventListener('resize', checkMobile)
  }
})

onUnmounted(() => {
  if (import.meta.client) {
    window.removeEventListener('resize', checkMobile)
  }
})
</script>
