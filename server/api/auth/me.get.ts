import { PrismaClient } from '@prisma/client'
import { getUserFromSession } from '~/server/utils/auth'

const prisma = new PrismaClient()

export default defineEventHandler(async (event) => {
  const session = getUserFromSession(event)
  if (!session) {
    return {
      authenticated: false,
      user: null
    }
  }

  try {
    const user = await prisma.user.findUnique({
      where: { id: session.userId }
    })

    if (!user) {
      return { authenticated: false, user: null }
    }

    return {
      authenticated: true,
      user: {
        id: user.id,
        name: user.name,
        email: user.email,
        avatar: user.avatar,
        xp: user.xp,
        streak: user.streak,
        provider: user.provider
      }
    }
  } catch (err) {
    return { authenticated: false, user: null }
  }
})
