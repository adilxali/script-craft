<template>
  <div class="min-h-screen flex bg-[#FFF7F4] text-slate-800 font-sans selection:bg-[#E76A4D] selection:text-white">
    <!-- Left Floating Sidebar (Desktop) -->
    <Sidebar class="hidden lg:flex" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-w-0">
      <TopNavbar @open-command-palette="$emit('open-command-palette')" />

      <main class="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from './Sidebar.vue'
import TopNavbar from './TopNavbar.vue'

defineEmits(['open-command-palette'])
</script>
