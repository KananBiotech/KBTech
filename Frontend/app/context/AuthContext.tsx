"use client"

import { createContext, useContext, useEffect, useState } from "react"

const AuthContext = createContext<any>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetch("/api/auth/me")
            .then(res => res.json())
            .then(data => {
                setUser(data.user)
                setLoading(false)
            })
    }, [])

    return (
        <AuthContext.Provider value={{ user, loading }}>
            {children}
        </AuthContext.Provider>
    )
}


export const useAuth = () => useContext(AuthContext)