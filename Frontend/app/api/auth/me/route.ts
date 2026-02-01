import { NextResponse } from "next/server"
import { getAuthCookie } from "@/app/lib/auth-cookies"

export async function GET() {
    const token = getAuthCookie()

    if (!token) {
        return NextResponse.json({ user: null }, { status: 401 })
    }

    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/auth/me/`, {
        headers: { Authorization: `Bearer ${token}` }
    })

    if (!res.ok) {
        return NextResponse.json({ user: null }, { status: 401 })
    }

    const user = await res.json()
    return NextResponse.json({ user })
}