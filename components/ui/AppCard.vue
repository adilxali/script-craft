<template>
  <div
    :class="[
      'bg-white rounded-[24px] border border-[#F2D8D2]/80 p-6 relative overflow-hidden transition-all duration-300 group',
      hoverable ? 'shadow-soft hover:shadow-[0_20px_45px_rgba(231,106,77,0.12)] hover:-translate-y-1 hover:border-[#E76A4D]/40' : 'shadow-soft',
      customClass
    ]"
  >
    <!-- Optional Soft Ambient Radial Glow -->
    <div
      v-if="glowColor === 'coral'"
      class="absolute -right-10 -top-10 w-36 h-36 bg-[#E76A4D]/10 rounded-full blur-2xl pointer-events-none group-hover:bg-[#E76A4D]/20 transition-all duration-300"
    />
    <div
      v-else-if="glowColor === 'amber'"
      class="absolute -right-10 -top-10 w-36 h-36 bg-[#F5A623]/10 rounded-full blur-2xl pointer-events-none group-hover:bg-[#F5A623]/20 transition-all duration-300"
    />
    <div
      v-else-if="glowColor === 'indigo'"
      class="absolute -right-10 -top-10 w-36 h-36 bg-[#6366F1]/10 rounded-full blur-2xl pointer-events-none group-hover:bg-[#6366F1]/20 transition-all duration-300"
    />
    <div
      v-else-if="glowColor === 'emerald'"
      class="absolute -right-10 -top-10 w-36 h-36 bg-[#10B981]/10 rounded-full blur-2xl pointer-events-none group-hover:bg-[#10B981]/20 transition-all duration-300"
    />

    <div class="relative z-10">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  hoverable?: boolean
  glowColor?: 'coral' | 'amber' | 'indigo' | 'emerald' | 'none'
  customClass?: string
}>()
</script>
