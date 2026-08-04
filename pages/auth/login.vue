<template>
  <div class="min-h-screen bg-[#FFF7F4] text-slate-800 flex items-center justify-center p-4 selection:bg-[#E76A4D] selection:text-white font-sans relative overflow-hidden">
    <!-- Ambient Glow -->
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[700px] h-[350px] bg-gradient-to-b from-[#E76A4D]/20 to-transparent blur-[120px] pointer-events-none rounded-full" />

    <div class="w-full max-w-md bg-white rounded-[28px] border border-[#F2D8D2] p-8 shadow-[0_20px_40px_rgba(0,0,0,0.06)] relative z-10">
      <!-- Header -->
      <div class="text-center mb-8">
        <NuxtLink to="/" class="inline-flex items-center gap-2 mb-4 group">
          <div class="w-10 h-10 rounded-2xl bg-[#E76A4D] flex items-center justify-center text-white shadow-md shadow-[#E76A4D]/25 group-hover:scale-105 transition-transform">
            <Play class="w-5 h-5 fill-white ml-0.5" />
          </div>
          <span class="font-extrabold text-xl text-slate-900 tracking-tight">ScriptCraft</span>
        </NuxtLink>

        <h1 class="text-2xl font-black text-slate-900 tracking-tight">Welcome Back</h1>
        <p class="text-xs text-slate-500 font-medium mt-1">Sign in to continue your JavaScript learning journey</p>
      </div>

      <!-- OAuth Login Buttons -->
      <div class="grid grid-cols-2 gap-3 mb-6">
        <button
          @click="handleOAuth('github')"
          class="w-full py-2.5 px-4 rounded-[16px] bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs shadow-sm transition-all flex items-center justify-center gap-2"
        >
          <Github class="w-4 h-4" />
          <span>GitHub</span>
        </button>

        <button
          @click="handleOAuth('google')"
          class="w-full py-2.5 px-4 rounded-[16px] bg-white border border-[#F2D8D2] hover:bg-[#FFF7F4] text-slate-800 font-bold text-xs shadow-sm transition-all flex items-center justify-center gap-2"
        >
          <Chrome class="w-4 h-4 text-rose-500" />
          <span>Google</span>
        </button>
      </div>

      <div class="relative flex items-center justify-center mb-6">
        <div class="w-full border-t border-[#F2D8D2]" />
        <span class="absolute bg-white px-3 text-[11px] text-slate-400 font-semibold uppercase">Or with Email</span>
      </div>

      <!-- Email / Password Form -->
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div v-if="errorMessage" class="p-3 rounded-2xl bg-rose-50 border border-rose-200 text-rose-600 text-xs font-semibold flex items-center gap-2">
          <AlertCircle class="w-4 h-4 shrink-0" />
          <span>{{ errorMessage }}</span>
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1.5">Email Address</label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="developer@scriptcraft.dev"
            class="w-full px-4 py-3 rounded-[16px] bg-[#FFF7F4] border border-[#F2D8D2] text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-[#E76A4D] transition-colors"
          />
        </div>

        <div>
          <div class="flex items-center justify-between mb-1.5">
            <label class="block text-xs font-bold text-slate-700">Password</label>
            <a href="#" class="text-[11px] text-[#E76A4D] font-bold hover:underline">Forgot?</a>
          </div>
          <input
            v-model="password"
            type="password"
            required
            placeholder="••••••••"
            class="w-full px-4 py-3 rounded-[16px] bg-[#FFF7F4] border border-[#F2D8D2] text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-[#E76A4D] transition-colors"
          />
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full py-3 px-4 rounded-[18px] bg-[#E76A4D] hover:bg-[#D85D3E] text-white font-extrabold text-xs shadow-md shadow-[#E76A4D]/25 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
        >
          <span>{{ isLoading ? 'Signing In...' : 'Sign In to Account' }}</span>
          <ArrowRight class="w-4 h-4" />
        </button>
      </form>

      <!-- Footer Link -->
      <div class="mt-8 text-center text-xs text-slate-500 font-medium">
        Don't have an account?
        <NuxtLink to="/auth/signup" class="text-[#E76A4D] font-bold hover:underline">Create Account</NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Play, Github, Chrome, AlertCircle, ArrowRight } from 'lucide-vue-next'
import { useAuthStore } from '~/stores/auth'

definePageMeta({
  middleware: 'auth'
})

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    await authStore.login(email.value, password.value)
    router.push('/dashboard')
  } catch (err: any) {
    errorMessage.value = err.data?.statusMessage || err.message || 'Login failed'
  } finally {
    isLoading.value = false
  }
}

async function handleOAuth(provider: 'github' | 'google') {
  isLoading.value = true
  errorMessage.value = ''
  try {
    await authStore.loginWithOAuth(provider)
    router.push('/dashboard')
  } catch (err: any) {
    errorMessage.value = 'OAuth authentication failed'
  } finally {
    isLoading.value = false
  }
}
</script>
