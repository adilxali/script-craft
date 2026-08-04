import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface UserProfile {
  id: string
  name: string
  email: string
  avatar?: string | null
  xp?: number
  streak?: number
  provider?: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<UserProfile | null>(null)
  const isInitialized = ref(false)

  const isAuthenticated = computed(() => !!user.value)

  async function fetchUser() {
    try {
      const res = await $fetch<{ authenticated: boolean; user: UserProfile | null }>('/api/auth/me')
      if (res.authenticated && res.user) {
        user.value = res.user
      } else {
        user.value = null
      }
    } catch (e) {
      user.value = null
    } finally {
      isInitialized.value = true
    }
  }

  async function signup(name: string, email: string, password: string) {
    const res = await $fetch<{ success: boolean; user: UserProfile }>('/api/auth/signup', {
      method: 'POST',
      body: { name, email, password }
    })
    if (res.success && res.user) {
      user.value = res.user
    }
    return res
  }

  async function login(email: string, password: string) {
    const res = await $fetch<{ success: boolean; user: UserProfile }>('/api/auth/login', {
      method: 'POST',
      body: { email, password }
    })
    if (res.success && res.user) {
      user.value = res.user
    }
    return res
  }

  async function loginWithOAuth(provider: 'github' | 'google') {
    const mockEmail = provider === 'github' ? 'dev-github@scriptcraft.dev' : 'dev-google@gmail.com'
    const mockName = provider === 'github' ? 'GitHub Developer' : 'Google Developer'
    const mockAvatar = provider === 'github'
      ? 'https://avatars.githubusercontent.com/u/9919?v=4'
      : 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=120&q=80'

    const res = await $fetch<{ success: boolean; user: UserProfile }>('/api/auth/oauth', {
      method: 'POST',
      body: {
        provider,
        email: mockEmail,
        name: mockName,
        avatar: mockAvatar,
        providerAccountId: `${provider}-${Date.now()}`
      }
    })
    if (res.success && res.user) {
      user.value = res.user
    }
    return res
  }

  async function logout() {
    try {
      await $fetch('/api/auth/logout', { method: 'POST' })
    } catch (e) {
      // Ignore
    }
    user.value = null
  }

  return {
    user,
    isInitialized,
    isAuthenticated,
    fetchUser,
    signup,
    login,
    loginWithOAuth,
    logout
  }
})
