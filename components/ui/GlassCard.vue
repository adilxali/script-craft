<template>
  <div
    :class="[
      'glass-card rounded-xl p-5 relative overflow-hidden group',
      hoverGlow ? 'hover:border-emerald-500/40 hover:shadow-emerald-500/10' : '',
      customClass
    ]"
  >
    <div
      v-if="glowColor === 'emerald'"
      class="absolute -right-12 -top-12 w-32 h-32 bg-emerald-500/10 rounded-full blur-2xl pointer-events-none group-hover:bg-emerald-500/20 transition-all"
    />
    <div
      v-else-if="glowColor === 'cyan'"
      class="absolute -right-12 -top-12 w-32 h-32 bg-cyan-500/10 rounded-full blur-2xl pointer-events-none group-hover:bg-cyan-500/20 transition-all"
    />
    <div
      v-else-if="glowColor === 'indigo'"
      class="absolute -right-12 -top-12 w-32 h-32 bg-indigo-500/10 rounded-full blur-2xl pointer-events-none group-hover:bg-indigo-500/20 transition-all"
    />

    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  glowColor?: 'emerald' | 'cyan' | 'indigo' | 'none'
  hoverGlow?: boolean
  customClass?: string
}>()
</script>
