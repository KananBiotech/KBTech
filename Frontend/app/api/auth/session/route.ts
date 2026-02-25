import { NextResponse } from 'next/server'
import { cookies } from 'next/headers'
import { decrypt } from '@/app/lib/sessions'

export async function GET() {
  const sessionCookie = (await cookies()).get('session')?.value
  const session = await decrypt(sessionCookie)

  if (!session?.user?.userId || !session?.user?.role) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 })
  }

  return NextResponse.json({
    expires_at: session.expiresAt,
    user_id: session.user.userId,
    role: session.user.role,
  })
}
