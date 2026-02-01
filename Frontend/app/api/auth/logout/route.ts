import { NextResponse } from "next/server"
import { deleteAuthCookie } from "@/app/lib/auth-cookies"

export async function POST() {
    deleteAuthCookie()
    return NextResponse.json({ success: true })
}