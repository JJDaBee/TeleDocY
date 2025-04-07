import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar: React.FC = () => {
    const navigate = useNavigate();

    const storedUser = sessionStorage.getItem('loggedInUser');
    const user = storedUser ? JSON.parse(storedUser) : null;

    const handleLogout = () => {
        sessionStorage.removeItem('loggedInUser');
        navigate('/login');
    };

    return (
        <nav
            style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '25px 180px 16px 32px',
                backgroundColor: '#007BFF',
                color: 'white',
                margin: '0px',
            }}
        >
            <h2 style={{ margin: 0 }}>
                <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>
                    TeleDocY
                </Link>
            </h2>

            <div style={{ display: 'flex', gap: '20px' }}>
                <Link to="/" style={linkStyle}>
                    Home
                </Link>
                <Link to="/symptom-checker" style={linkStyle}>
                    Symptom Checker
                </Link>

                {user?.role === 'doctor' && (
                    <>
                        <Link to="/dashboard" style={linkStyle}>
                            Dashboard
                        </Link>
                        <span
                            onClick={handleLogout}
                            style={{ ...linkStyle, cursor: 'pointer' }}
                        >
                            Logout
                        </span>
                    </>
                )}

                {user?.role === 'patient' && (
                    <>
                        <Link to="/consultation" style={linkStyle}>
                            Consultation
                        </Link>
                        <Link to="/payment" style={linkStyle}>
                            Payment
                        </Link>
                        <span
                            onClick={handleLogout}
                            style={{ ...linkStyle, cursor: 'pointer' }}
                        >
                            Logout
                        </span>
                    </>
                )}

                {!user && (
                    <Link to="/login" style={linkStyle}>
                        Login
                    </Link>
                )}
            </div>
        </nav>
    );
};

const linkStyle: React.CSSProperties = {
    color: 'white',
    textDecoration: 'none',
    fontSize: '1rem',
    fontWeight: 500,
};

export default Navbar;
