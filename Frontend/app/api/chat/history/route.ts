import { NextResponse } from 'next/server'
import { cookies, headers } from 'next/headers'
import { decrypt } from '@/app/lib/sessions'

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

async function userId() {
  const session = await decrypt((await cookies()).get('session')?.value)
  if (session?.user?.userId) return session.user.userId
  const visitorId = (await headers()).get('x-chat-visitor-id') || ''
  return /^[a-zA-Z0-9-]{8,100}$/.test(visitorId) ? `guest:${visitorId}` : null
}

export async function GET() {
  const id = await userId()
  if (!id) return NextResponse.json({ messages: [] })
  const response = await fetch(`${backendUrl}/api/ai/chat/history/?user_id=${encodeURIComponent(id)}`, { cache: 'no-store' })
  return NextResponse.json(await response.json(), { status: response.status })
}

export async function DELETE() {
  const id = await userId()
  if (!id) return NextResponse.json({ status: 'cleared' })
  const response = await fetch(`${backendUrl}/api/ai/chat/history/clear/?user_id=${encodeURIComponent(id)}`, { method: 'DELETE' })
  return NextResponse.json(await response.json(), { status: response.status })
}
