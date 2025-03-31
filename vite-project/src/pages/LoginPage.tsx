// src/pages/LoginPage.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

type User = {
    username: string;
    password: string;
    role: 'patient' | 'doctor';
};

type LoginPageProps = {
    setUser: (user: User) => void;
};

const accounts: User[] = [
    { username: 'p1', password: '111', role: 'patient' },
    { username: 'd1', password: '111', role: 'doctor' },
];

const LoginPage: React.FC<LoginPageProps> = ({ setUser }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = () => {
        const user = accounts.find(
            (acc) => acc.username === username && acc.password === password
        );

        if (user) {
            setUser(user);
            navigate(user.role === 'doctor' ? '/dashboard' : '/');
        } else {
            setError('Invalid credentials');
        }
    };

    return (
        <div style={{ padding: 20 }}>
            <h2>Login</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <br />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <br />
            <button onClick={handleLogin}>Login</button>
            <div>
                <h3>Test Accounts</h3>
                <ul>
                    <li>Patient: p1 / 111</li>
                    <li>Doctor: d1 / 111</li>
                </ul>
            </div>
        </div>
    );
};

export default LoginPage;
