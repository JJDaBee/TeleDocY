import React, { useState } from 'react';
import Navbar from '../components/navbar';
import Footer from '../components/footer';

const Consultation: React.FC = () => {
    const [symptom, setSymptom] = useState('');
    const participantName = 'Alice'; // Replace with user context if needed

    const handleConsult = async () => {
        if (!symptom.trim()) {
            alert('Please describe your symptom before joining.');
            return;
        }

        try {
            // TODO: Post to symptom microservice
            /*
            await fetch('http://localhost:YOUR_MICROSERVICE/symptom', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    patient: participantName,
                    symptom,
                    timestamp: new Date().toISOString(),
                }),
            });
            */


            /*don't touch */
            const res = await fetch('http://localhost:5000/create-token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ participantName }),
            });
            if (!res.ok) {
                throw new Error('Failed to create token');
            }

            const { authToken } = await res.json();


            const meetingURL = `/meeting?authToken=${authToken}&symptom=${encodeURIComponent(symptom)}`;
            window.open(meetingURL, '_blank');
        } catch (error) {
            console.error('❌ Error:', error);
            alert('Unable to join the consultation. Please try again.');
        }
    };

    return (
        <>
            <Navbar />

            <section
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                    padding: '20px 0px',
                    textAlign: 'center',
                    background: 'linear-gradient(to right, #f9f9f9, #e8f0ff)',
                    minHeight: '100vh',
                    minWidth: '100vw',
                    overflowX: 'hidden',
                    margin: 0,
                }}
            >
                <h1 style={{ fontSize: '2.5rem', marginBottom: '20px', color: '#333' }}>
                    Start Your Consultation
                </h1>

                <label htmlFor="symptom" style={{ marginBottom: '8px', fontSize: '1rem' , color:'#333'}}>
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
