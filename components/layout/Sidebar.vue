<template>
  <aside class="w-72 h-[calc(100vh-2rem)] sticky top-4 my-4 ml-4 bg-white rounded-[28px] border border-[#F2D8D2]/80 shadow-[0_10px_30px_rgba(0,0,0,0.06)] flex flex-col justify-between p-5 z-30 shrink-0 font-sans">
    <!-- Top Section: Brand & Nav Links -->
    <div class="space-y-5 overflow-y-auto pr-1">
      <!-- Logo Header -->
      <NuxtLink to="/" class="flex items-center gap-3 px-2 group">
        <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-[#E76A4D] to-[#F08C6A] flex items-center justify-center text-white shadow-md shadow-[#E76A4D]/25 group-hover:scale-105 transition-transform">
          <Play class="w-5 h-5 fill-white ml-0.5" />
        </div>
        <div class="flex flex-col">
          <span class="font-extrabold text-base tracking-tight text-slate-800">
            ScriptCraft
          </span>
          <span class="text-[10px] text-slate-400 font-medium tracking-wide uppercase -mt-0.5">
            Student Dashboard
          </span>
        </div>
      </NuxtLink>

      <!-- DYNAMIC SIDEBAR: LEARN JAVASCRIPT CURRICULUM MODE -->
      <div v-if="$route.path.startsWith('/learn')" class="space-y-4">
        <!-- Back to Dashboard Link -->
        <NuxtLink
          to="/dashboard"
          class="flex items-center gap-2 px-3 py-2 rounded-xl bg-[#FFF7F4] border border-[#F2D8D2] text-[#E76A4D] hover:bg-[#E76A4D]/10 text-xs font-bold transition-all"
        >
          <ChevronLeft class="w-4 h-4" />
          <span>Back to Main Menu</span>
        </NuxtLink>

        <div>
          <h4 class="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 mb-3 font-mono flex items-center justify-between">
            <span>COURSE CURRICULUM</span>
            <BookOpen class="w-3.5 h-3.5 text-[#E76A4D]" />
          </h4>

          <!-- Modules List -->
          <div class="space-y-3">
            <div
              v-for="mod in curriculumModules"
              :key="mod.id"
              class="rounded-2xl border border-[#F2D8D2]/70 overflow-hidden bg-white shadow-sm"
            >
              <!-- Module Accordion Header -->
              <button
                @click="toggleModule(mod.id)"
                class="w-full px-3.5 py-2.5 bg-[#FFF7F4] hover:bg-[#FFF0EB] flex items-center justify-between text-left transition-colors"
              >
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-lg bg-[#E76A4D]/10 text-[#E76A4D] font-mono font-bold text-[11px] flex items-center justify-center">
                    0{{ mod.order }}
                  </span>
                  <div>
                    <h5 class="text-xs font-extrabold text-slate-900 leading-tight">{{ mod.title }}</h5>
                    <p class="text-[10px] text-slate-400 font-medium">{{ mod.lessons.length }} Lessons</p>
                  </div>
                </div>
                <ChevronDown
                  class="w-4 h-4 text-slate-400 transition-transform duration-200"
                  :class="openModules.includes(mod.id) ? 'rotate-180 text-[#E76A4D]' : ''"
                />
              </button>

              <!-- Module Lessons Tree -->
              <div v-show="openModules.includes(mod.id)" class="p-1.5 space-y-1 bg-white">
                <NuxtLink
                  v-for="lesson in mod.lessons"
                  :key="lesson.path"
                  :to="lesson.path"
                  :class="[
                    'flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all',
                    $route.path === lesson.path
                      ? 'bg-[#E76A4D] text-white font-bold shadow-sm'
                      : 'text-slate-600 hover:text-[#E76A4D] hover:bg-[#FFF7F4]'
                  ]"
                >
                  <div class="flex items-center gap-2 overflow-hidden">
                    <FileCode class="w-3.5 h-3.5 shrink-0" />
                    <span class="truncate">{{ lesson.title }}</span>
                  </div>

                  <CheckCircle2
                    v-if="progressStore.isLessonCompleted(lesson.key)"
                    :class="$route.path === lesson.path ? 'text-white' : 'text-emerald-500'"
                    class="w-3.5 h-3.5 shrink-0"
                  />
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- STANDARD MAIN MENU MODE -->
      <template v-else>
        <!-- Main Menu Section -->
        <div>
          <h4 class="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 mb-2 font-mono">
            MAIN MENU
          </h4>

          <nav class="space-y-1">
            <NuxtLink
              v-for="item in mainMenu"
              :key="item.path"
              :to="item.path"
              :class="[
                'flex items-center gap-3 px-3.5 py-2.5 rounded-[18px] text-xs font-semibold transition-all duration-200',
                $route.path === item.path || ($route.path.startsWith(item.path) && item.path !== '/')
                  ? 'bg-[#E76A4D] text-white shadow-md shadow-[#E76A4D]/25 font-bold'
                  : 'text-slate-600 hover:text-[#E76A4D] hover:bg-[#FFF7F4]'
              ]"
            >
              <component :is="item.icon" class="w-4 h-4" />
              <span>{{ item.name }}</span>
            </NuxtLink>
          </nav>
        </div>

        <!-- Other Menu Section -->
        <div>
          <h4 class="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 mb-2 font-mono">
            OTHER MENU
          </h4>

          <nav class="space-y-1">
            <NuxtLink
              v-for="item in otherMenu"
              :key="item.path"
              :to="item.path"
              class="flex items-center gap-3 px-3.5 py-2.5 rounded-[18px] text-xs font-semibold text-slate-600 hover:text-[#E76A4D] hover:bg-[#FFF7F4] transition-all"
            >
              <component :is="item.icon" class="w-4 h-4" />
              <span>{{ item.name }}</span>
            </NuxtLink>
          </nav>
        </div>
      </template>

      <!-- Mode Switcher -->
      <div>
        <h4 class="text-[11px] font-bold uppercase tracking-wider text-slate-400 px-3 mb-2 font-mono">
          MODE
        </h4>
        <div class="flex items-center p-1 bg-[#FFF7F4] border border-[#F2D8D2] rounded-full">
          <button
            @click="isDark = false"
            :class="[
              'flex-1 py-1.5 rounded-full text-xs font-semibold flex items-center justify-center gap-1.5 transition-all',
              !isDark ? 'bg-slate-900 text-white shadow-sm' : 'text-slate-500 hover:text-slate-800'
            ]"
          >
            <Sun class="w-3.5 h-3.5" />
            <span>Light</span>
          </button>
          <button
            @click="isDark = true"
            :class="[
              'flex-1 py-1.5 rounded-full text-xs font-semibold flex items-center justify-center gap-1.5 transition-all',
              isDark ? 'bg-slate-900 text-white shadow-sm' : 'text-slate-500 hover:text-slate-800'
            ]"
          >
            <Moon class="w-3.5 h-3.5" />
            <span>Dark</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Bottom User Section -->
    <div class="pt-4 border-t border-[#F2D8D2]/60 flex items-center justify-between">
      <div class="flex items-center gap-2.5 overflow-hidden">
        <img
          :src="authStore.user?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80'"
          :alt="authStore.user?.name || 'User'"
          class="w-9 h-9 rounded-full object-cover border border-[#E76A4D] shrink-0"
        />
        <div class="flex flex-col overflow-hidden">
          <span class="text-xs font-bold text-slate-800 truncate max-w-[110px]">{{ authStore.user?.name || 'Guest User' }}</span>
          <span class="text-[10px] text-slate-400 font-medium truncate max-w-[110px]">{{ authStore.user?.email || 'Pro Student' }}</span>
        </div>
      </div>

      <button
        @click="handleLogout"
        class="p-2 rounded-xl text-slate-400 hover:text-[#E76A4D] hover:bg-[#FFF7F4] transition-colors shrink-0"
        title="Logout"
      >
        <LogOut class="w-4 h-4" />
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  Play,
  LayoutDashboard,
  BookOpen,
  Code2,
  Trophy,
  BarChart3,
  HelpCircle,
  Settings,
  Sun,
  Moon,
  LogOut,
  CheckSquare,
  Bookmark,
  Users,
  Award,
  ChevronLeft,
  ChevronDown,
  FileCode,
  CheckCircle2
} from 'lucide-vue-next'
import { useAuthStore } from '~/stores/auth'
import { useProgressStore } from '~/stores/progress'

const router = useRouter()
const authStore = useAuthStore()
const progressStore = useProgressStore()

const isDark = ref(false)
const openModules = ref<string[]>(['mod-1', 'mod-2'])

function toggleModule(id: string) {
  if (openModules.value.includes(id)) {
    openModules.value = openModules.value.filter(m => m !== id)
  } else {
    openModules.value.push(id)
  }
}

async function handleLogout() {
  await authStore.logout()
  router.push('/auth/login')
}

const curriculumModules = [
  {
    id: 'mod-1',
    order: 1,
    title: 'JS Foundations & Scope',
    lessons: [
      {
        title: 'Closures & Lexical Scope',
        key: '01-foundations/01-closures',
        path: '/learn/01-foundations/01-closures'
      },
      {
        title: 'Async Promises & Event Loop',
        key: '01-foundations/02-async-promises',
        path: '/learn/01-foundations/02-async-promises'
      }
    ]
  },
  {
    id: 'mod-2',
    order: 2,
    title: 'Prototypes & OOP',
    lessons: [
      {
        title: 'Prototype Chain & Inheritance',
        key: '02-prototypes/01-prototype-chain',
        path: '/learn/02-prototypes/01-prototype-chain'
      }
    ]
  }
]

const mainMenu = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Learn JavaScript', path: '/learn/01-foundations/01-closures', icon: BookOpen },
  { name: 'Playground', path: '/playground', icon: Code2 },
  { name: 'Challenges', path: '/dashboard', icon: CheckSquare },
  { name: 'Progress', path: '/dashboard', icon: BarChart3 },
  { name: 'Certificates', path: '/dashboard', icon: Award },
  { name: 'Community', path: '/dashboard', icon: Users },
  { name: 'Bookmarks', path: '/dashboard', icon: Bookmark }
]

const otherMenu = [
  { name: 'Help Center', path: '/dashboard', icon: HelpCircle },
  { name: 'Settings', path: '/dashboard', icon: Settings }
]
</script>
