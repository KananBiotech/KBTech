import { cookies } from "next/headers"

export async function setAuthCookie(token: string) {
    (await cookies()).set({
        name: process.env.JWT_COOKIE_NAME!,
        value: token,
        httpOnly: true,
        secure: true,
        sameSite: "strict",
        path: "/"
    })
}


export async function deleteAuthCookie() {
    (await cookies()).delete(process.env.JWT_COOKIE_NAME!)
}


export async function getAuthCookie() {
    return (await cookies()).get(process.env.JWT_COOKIE_NAME!)?.value
}