import 'server-only'
 
import { cookies } from 'next/headers'
import { decrypt } from './sessions'
import { cache } from 'react'
import { redirect } from 'next/dist/client/components/navigation'
import { SessionPayload } from '../types'
 
export const verifySession = cache(async () => {
  const cookie = (await cookies()).get('session')?.value
  const session = await decrypt(cookie) as SessionPayload
 
  if (!session?.user?.userId || !session?.user?.role) {
    redirect('/login')
  }
 
  return { isAuth: true, userId: session.user.userId, role: session.user.role }
})