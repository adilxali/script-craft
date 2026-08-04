import { getUserFromSession } from '~/server/utils/auth'

export default defineEventHandler((event) => {
  const path = getRequestPath(event)

  // Protected API routes requiring valid JWT session
  const protectedPaths = ['/api/progress', '/api/submissions']

  const isProtected = protectedPaths.some(p => path.startsWith(p))

  if (isProtected) {
    const session = getUserFromSession(event)
    if (!session) {
      throw createError({
        statusCode: 401,
        statusMessage: 'Unauthorized access. Valid session token required.'
      })
    }
    // Attach session to event context for downstream handlers
    event.context.user = session
  }
})
