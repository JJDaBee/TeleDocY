import React from 'react';
import { Link } from 'react-router-dom';


const Navbar: React.FC = () => {
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
                    TeleDoc
                </Link>
            </h2>

            <div style={{ display: 'flex', gap: '20px' }}>
                <Link to="/" style={linkStyle}>Home</Link>
                <Link to="/consultation" style={linkStyle}>Consultation</Link>
                <Link to="/dashboard" style={linkStyle}>Dashboard</Link>
                <Link to="/symptom-checker" style={linkStyle}>Symptom Checker</Link>
                <Link to="/login" style={linkStyle}>Login</Link>
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


