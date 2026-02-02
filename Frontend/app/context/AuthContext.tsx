"use client"

import React, { createContext, useContext, useEffect, useState } from "react"
import { SessionContext } from "../types"
import axios from "axios"

type AuthContextType = {
    user: SessionContext | null,
    setUser: React.Dispatch<React.SetStateAction<SessionContext | null>>
    loading: boolean
}

export const AuthContext = createContext<AuthContextType>({
    user: null,
    setUser: (() => {}),
    loading: false
})


export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<SessionContext | null>(null)
    const [loading, setLoading] = useState(true)
    
    useEffect(() => {
        axios.get(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/auth/verify/`, {
            withCredentials: true,
        })
            .then(res => {
                setUser({
                    expiresAt: res.data.expires_at,
                    user: {
                        userId: res.data.user_id,
                        role: res.data.role
                    }
                });
            })
            .catch(err => {
                setUser(null);
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);


    return (
        <AuthContext.Provider value={{ user, setUser, loading }}>
            {children}
        </AuthContext.Provider>
    )
}


export const useAuth = () => useContext<AuthContextType>(AuthContext)