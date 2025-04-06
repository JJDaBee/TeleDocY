// src/pages/LoginPage.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/navbar';
import Footer from '../components/footer';


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
    {
        username: "Goh Zhi Hao",
        password: "111",
        role: "doctor"
      },
      
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
        <>
            <Navbar />
            <div
                style={{
                    minHeight: '100vh',
                    width:'100vw',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: 'linear-gradient(to right, #f9f9f9, #e8f0ff)',
                    padding: '40px 0px',
                    margin: '0 auto'
                }}
            >
                <div
                    style={{
                        backgroundColor: 'white',
                        padding: '40px',
                        borderRadius: '12px',
                        boxShadow: '0 0 20px rgba(0,0,0,0.1)',
                        maxWidth: '400px',
                        width: '100%',
                        textAlign: 'center',
                    }}
                >
                    <h2 style={{ marginBottom: '24px' , margin:'0 auto', color: '#007BFF' }}>Login to <span style={{ color: '#007BFF' }}>TeleDoc</span></h2>

                    {error && <p style={{ color: 'red', marginBottom: '16px' }}>{error}</p>}

                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        style={inputStyle}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={inputStyle}
                    />

                    <button
                        onClick={handleLogin}
                        style={{
                            marginTop: '20px',
                            padding: '12px 24px',
                            width: '50%',
                            fontSize: '1rem',
                            backgroundColor: '#007BFF',
                            color: 'white',
                            border: 'none',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            margin: '10 auto'
                        }}
                    >
                        Login
                    </button>

                    <div style={{ marginTop: '30px', textAlign: 'left' }}>
                        <h4>Test Accounts</h4>
                        <ul style={{ paddingLeft: '20px', color: '#555' }}>
                            <li>👤 Patient: <strong>p1 / 111</strong></li>
                            <li>🩺 Doctor: <strong>d1 / 111</strong></li>
                        </ul>
                    </div>
                </div>
            </div>
            <Footer />
        </>
    );
};

const inputStyle: React.CSSProperties = {
    width: '100%',
    padding: '12px',
    margin: '0 auto',
    border: '1px solid #ccc',
    borderRadius: '8px',
    fontSize: '1rem',
};

export default LoginPage;
