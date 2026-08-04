import jwt from 'jsonwebtoken'
import { H3Event, parseCookies, setCookie, deleteCookie } from 'h3'

const JWT_SECRET = process.env.JWT_SECRET || 'scriptcraft-production-secret-jwt-key-2026'
const TOKEN_MAX_AGE = 60 * 60 * 24 * 7 // 7 days

export interface AuthPayload {
  userId: string
  email: string
  name: string
  role?: string
  avatar?: string | null
}

export function signJwtToken(payload: AuthPayload): string {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: '7d' })
}

export function verifyJwtToken(token: string): AuthPayload | null {
  try {
    return jwt.verify(token, JWT_SECRET) as AuthPayload
  } catch (err) {
    return null
  }
}

export function setAuthCookie(event: H3Event, token: string) {
  setCookie(event, 'scriptcraft_session', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: TOKEN_MAX_AGE,
    path: '/'
  })
}

export function clearAuthCookie(event: H3Event) {
  deleteCookie(event, 'scriptcraft_session', { path: '/' })
}

export function getUserFromSession(event: H3Event): AuthPayload | null {
  const cookies = parseCookies(event)
  const token = cookies.scriptcraft_session
  if (!token) return null
  return verifyJwtToken(token)
}
