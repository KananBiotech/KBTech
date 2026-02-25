import { NextRequest, NextResponse } from 'next/server'
import { decrypt } from './app/lib/sessions'
 
// 1. Specify protected and auth-only routes
const protectedRoutePrefixes = ['/dashboard', '/account', '/history']
const authOnlyRoutes = ['/login', '/signup', '/forgot-password']
 
export default async function proxy(req: NextRequest) {
  // 2. Check if the current route is protected or public
  const path = req.nextUrl.pathname
  const isProtectedRoute = protectedRoutePrefixes.some((route) => path.startsWith(route))
  const isAuthOnlyRoute = authOnlyRoutes.includes(path)
 
  // 3. Decrypt the session from the cookie
  const cookie = req.cookies.get('session')?.value
  const session = await decrypt(cookie)
 
  // 4. Redirect to /login if the user is not authenticated
  if (isProtectedRoute && !session?.user?.userId) {
    return NextResponse.redirect(new URL('/login', req.nextUrl))
  }
 
  // 5. Redirect to /dashboard if the user is authenticated and opens auth pages
  if (
    isAuthOnlyRoute &&
    session?.user?.userId &&
    !req.nextUrl.pathname.startsWith('/dashboard')
  ) {
    return NextResponse.redirect(new URL('/dashboard', req.nextUrl))
  }
 
  return NextResponse.next()
}
 
// Routes Proxy should not run on
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
}
