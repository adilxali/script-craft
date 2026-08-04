import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore()

  // Initialize session from server if not already done
  if (!authStore.isInitialized) {
    await authStore.fetchUser()
  }

  // Routes requiring authentication
  const protectedRoutes = ['/dashboard', '/playground', '/learn']

  // Auth pages (login, signup)
  const authRoutes = ['/auth/login', '/auth/signup']

  const isProtectedRoute = protectedRoutes.some(r => to.path.startsWith(r))
  const isAuthRoute = authRoutes.some(r => to.path.startsWith(r))

  if (isProtectedRoute && !authStore.isAuthenticated) {
    return navigateTo(`/auth/login?redirect=${encodeURIComponent(to.fullPath)}`)
  }

  if (isAuthRoute && authStore.isAuthenticated) {
    return navigateTo('/dashboard')
  }
})
