import bcrypt from 'bcryptjs'
import { PrismaClient } from '@prisma/client'
import { signJwtToken, setAuthCookie } from '~/server/utils/auth'

const prisma = new PrismaClient()

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { name, email, password } = body

  if (!name || !email || !password) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Name, email, and password are required'
    })
  }

  // Check if user already exists
  const existingUser = await prisma.user.findUnique({
    where: { email }
  })

  if (existingUser) {
    throw createError({
      statusCode: 400,
      statusMessage: 'An account with this email already exists'
    })
  }

  // Hash password
  const passwordHash = await bcrypt.hash(password, 10)

  // Create user in DB
  const user = await prisma.user.create({
    data: {
      name,
      email,
      passwordHash,
      provider: 'credentials',
      avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(name)}`
    }
  })

  // Sign JWT
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
      streak: user.streak
    }
  }
})
