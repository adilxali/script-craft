<template>
  <AppCard custom-class="h-full flex flex-col justify-between">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-base font-extrabold text-slate-900">Top Mentors</h3>
      <button class="text-xs font-bold text-[#E76A4D] hover:underline">
        View all
      </button>
    </div>

    <!-- Mentors List -->
    <div class="space-y-3">
      <div
        v-for="mentor in mentors"
        :key="mentor.name"
        class="flex items-center justify-between p-2 rounded-2xl hover:bg-[#FFF7F4] transition-colors"
      >
        <div class="flex items-center gap-3">
          <img
            :src="mentor.avatar"
            :alt="mentor.name"
            class="w-9 h-9 rounded-full object-cover border border-[#F2D8D2]"
          />
          <div>
            <h4 class="text-xs font-extrabold text-slate-900 leading-snug">{{ mentor.name }}</h4>
            <p class="text-[11px] text-slate-400 font-medium">{{ mentor.role }}</p>
          </div>
        </div>

        <button class="text-slate-400 hover:text-slate-600 p-1">
          <MoreVertical class="w-4 h-4" />
        </button>
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { MoreVertical } from 'lucide-vue-next'
import AppCard from '~/components/ui/AppCard.vue'

const mentors = [
  {
    name: 'Abraham Kolin',
    role: 'Lead product designer at @pixelean',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=120&q=80'
  },
  {
    name: 'Julia Eve',
    role: 'Design director at @apple',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=120&q=80'
  },
  {
    name: 'Chester Lofus',
    role: 'Marketing director at @samsung',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=120&q=80'
  },
  {
    name: 'Maxwell Reed',
    role: 'Full stack developer at @scriptcraft',
    avatar: 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=120&q=80'
  },
  {
    name: 'Sophie Lane',
    role: 'Design director at @zara',
    avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=120&q=80'
  }
]
</script>
