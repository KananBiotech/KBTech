export type UserData = {
    firstName: string,
    lastName: string,
    email: string,
    phone: string,
    state: string,
    password: string,
    confirmPassword: string,
    farmType: string,
}

export type SessionPayload = {
    expiresAt: Date
    user: {
        password: string
        userId: string
        email: string
        role: "admin" | "user"
    }
}