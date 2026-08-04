import { PrismaClient } from '@prisma/client'
import { signJwtToken, setAuthCookie } from '~/server/utils/auth'

const prisma = new PrismaClient()

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { provider, email, name, avatar, providerAccountId } = body

  if (!provider || !email || !name) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Provider, email, and name are required'
    })
  }

  // Find or create user for OAuth
  let user = await prisma.user.findUnique({
    where: { email }
  })

  if (!user) {
    user = await prisma.user.create({
      data: {
        email,
        name,
        avatar: avatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(name)}`,
        provider,
        providerAccountId: providerAccountId || `${provider}-${Date.now()}`
      }
    })
  }

  const token = signJwtToken({
    userId: user.id,
    email: user.email,
    name: user.name,
    avatar: user.avatar
  })

  setAuthCookie(event, token)

  return {
    success: true,
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
})
