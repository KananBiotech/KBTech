import React, { useTransition } from "react";
import { useAuth } from "../context/AuthContext";
import { logout } from "../actions/auth";

const Logout = () => {

    const { setUser } = useAuth()
    const [isPending, startTransition] = useTransition()

    const handleLogout = async () => {
        setUser(null);
        startTransition(async () => {
            await logout();
        });
    };

    return (
        <button
            onClick={() => void handleLogout()}
            disabled={isPending}
            className="rounded-lg bg-red-500 px-4 py-2 text-sm font-semibold text-white
                       transition-colors duration-200 hover:bg-red-600
                       focus:outline-none focus:ring-2 focus:ring-red-400
                       active:bg-red-700"
        >
            Logout
        </button>
    );
};

export default Logout;
