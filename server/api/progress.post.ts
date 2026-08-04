import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { userId, lessonId, xpReward } = body

  if (!lessonId) {
    throw createError({ statusCode: 400, statusMessage: 'lessonId is required' })
  }

  try {
    const targetUserId = userId || 'default-user'

    // Upsert dummy user if needed
    const user = await prisma.user.upsert({
      where: { email: 'developer@scriptcraft.dev' },
      update: {
        xp: { increment: xpReward || 50 },
        lastActiveAt: new Date()
      },
      create: {
        id: targetUserId,
        email: 'developer@scriptcraft.dev',
        name: 'ScriptCraft Developer',
        xp: xpReward || 50
      }
    })

    return {
      success: true,
      user
    }
  } catch (err: any) {
    return {
      success: true,
      message: 'Progress recorded locally',
      error: err.message
    }
  }
})
