import { NextResponse } from "next/server"
import { setAuthCookie } from "@/app/lib/auth-cookies"

export async function POST(req: Request) {
    const body = await req.json()

    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/auth/register/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    })


    if (!res.ok) {
        return NextResponse.json({ error: "Registration failed" }, { status: 400 })
    }


    const data = await res.json()
    setAuthCookie(data.access)


    return NextResponse.json({ success: true })
}