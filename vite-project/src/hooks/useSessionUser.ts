// src/hooks/useSessionUser.ts
import { useEffect, useState } from 'react';

type User = {
    username: string;
    password: string;
    role: 'patient' | 'doctor';
    uuid?: string;
    doctorName?: string;
};

const useSessionUser = (): User | null => {
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        const storedUser = sessionStorage.getItem('loggedInUser');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
    }, []);

    return user;
};

export default useSessionUser;
