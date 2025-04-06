import React, { useState } from 'react';
import Navbar from '../components/navbar';
import Footer from '../components/footer';

const Consultation: React.FC = () => {
    const [symptom, setSymptom] = useState('');
    const uuid = 'uuid-1234'; // TODO: Replace with actual user uuid

    const handleConsult = () => {
        if (!symptom.trim()) {
            alert('Please describe your symptom before joining.');
            return;
        }

        sessionStorage.setItem('symptom', symptom);
        sessionStorage.setItem('uuid', uuid);

        //  Go to loader
        window.open(`/loader`, '_blank');

    };

    return (
        <>
            <Navbar />
            <section style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                padding: '20px 0',
                background: 'linear-gradient(to right, #f9f9f9, #e8f0ff)',
                minHeight: '100vh',
                width: '100vw',
            }}>
                <h1 style={{ fontSize: '2.5rem', color: '#333' }}>Start Your Consultation</h1>
                <label htmlFor="symptom" style={{ marginTop: '20px', marginBottom: '8px', fontSize: '1rem', color: '#333' }}>
                    Describe your symptom:
                </label>
                <textarea
                    id="symptom"
                    rows={4}
                    value={symptom}
                    onChange={(e) => setSymptom(e.target.value)}
                    placeholder="e.g. I've been having headaches and chills..."
                    style={{
                        width: '100%',
                        maxWidth: '600px',
                        padding: '12px',
                        borderRadius: '8px',
                        border: '1px solid #ccc',
                        marginBottom: '24px',
                        fontSize: '1rem',
                    }}
                />
                <button
                    onClick={handleConsult}
                    style={{
                        padding: '12px 24px',
                        fontSize: '1rem',
                        backgroundColor: '#007BFF',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        cursor: 'pointer',
                    }}
                >
                    Join Consultation
                </button>
            </section>
            <Footer />
        </>
    );
};

export default Consultation;
