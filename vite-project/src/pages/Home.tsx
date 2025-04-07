import React from 'react';
// Placeholder components — create them later
import Navbar from '../components/navbar';
import Footer from '../components/footer';
const Home: React.FC = () => {
    return (
        <>
            <Navbar />

            <section
    style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0px 0px',
        textAlign: 'center',
        background: 'linear-gradient(to right, #f9f9f9, #e8f0ff)',
        minHeight: '100vh', // ✅ full screen height
        minWidth: '100vw', 
        overflowX: 'hidden',
        margin: '0px'
    }}
>

                <h1 style={{ fontSize: '3rem', marginBottom: '20px', color: '#333' }}>
                    Welcome to <span style={{ color: '#007BFF' }}>TeleDocY</span>
                </h1>
                <p style={{ fontSize: '1.25rem', maxWidth: '600px', color: '#555' }}>
                    Get trusted medical help from certified doctors — anytime, anywhere.
                    Book consultations, track your prescriptions, and manage your health online.
                </p>

                <div style={{ marginTop: '40px', display: 'flex', gap: '20px' }}>
                    <button
                        style={{
                            padding: '12px 24px',
                            fontSize: '1rem',
                            backgroundColor: '#007BFF',
                            color: 'white',
                            border: 'none',
                            borderRadius: '8px',
                            cursor: 'pointer',
                        }}
                        onClick={() => window.location.href = '/login'}
                    >
                        Get Started
                    </button>
                    <button
                        style={{
                            padding: '12px 24px',
                            fontSize: '1rem',
                            backgroundColor: 'white',
                            border: '2px solid #007BFF',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            color: '#007BFF',
                        }}
                        onClick={() => window.location.href = '/symptom-checker'}
                    >
                        Try Symptom Checker
                    </button>
                </div>
            </section>

            <Footer />
        </>
    );
};

export default Home;
