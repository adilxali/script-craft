<template>
  <AppCard custom-class="h-full flex flex-col justify-between overflow-hidden bg-gradient-to-b from-white to-[#FFF7F4]">
    <div>
      <h3 class="text-xl font-black text-slate-900 leading-tight mb-3">
        Keep Learning New Things Everyday
      </h3>
      <p class="text-xs text-slate-500 leading-relaxed">
        Get ready for an exciting journey into new knowledge! This exploration promises to be enlightening and enriching.
      </p>
    </div>

    <!-- Student Image & CTA -->
    <div class="mt-6 flex flex-col items-center">
      <div class="w-full h-44 rounded-2xl overflow-hidden relative mb-4 shadow-sm">
        <img
          src="https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=600&q=80"
          alt="Student learning"
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-slate-900/60 to-transparent flex items-end p-3">
          <span class="text-[11px] font-bold text-white">Join 12,000+ Active Students</span>
        </div>
      </div>

      <button class="w-full py-3 px-4 rounded-[18px] bg-slate-900 hover:bg-slate-800 text-white font-extrabold text-xs shadow-md transition-all flex items-center justify-center gap-2">
        <span>Join community</span>
        <Plus class="w-4 h-4" />
      </button>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { Plus } from 'lucide-vue-next'
import AppCard from '~/components/ui/AppCard.vue'
</script>
