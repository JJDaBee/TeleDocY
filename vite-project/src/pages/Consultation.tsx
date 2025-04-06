import React, { useState } from 'react';
import Navbar from '../components/navbar';
import Footer from '../components/footer';

const Consultation: React.FC = () => {
    const [symptom, setSymptom] = useState('');
    const [loading, setLoading] = useState(false);
    const [doctor, setDoctor] = useState<{
        name: string;
        gender: string;
        picture: string;
    }>({ name: '', gender: '', picture: '' });

    const storedUser = sessionStorage.getItem('loggedInUser');
    const parsedUser = storedUser ? JSON.parse(storedUser) : null;
    const uuid = parsedUser?.uuid;

    const handleConsult = async () => {
        if (!symptom.trim()) {
            alert('Please describe your symptom before joining.');
            return;
        }

        setLoading(true);

        try {
            const res = await fetch('http://localhost:5100/book_consult', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ uuid, reasonForVisit: symptom }),
            });

            const data = await res.json();
            const token = data.dyte_token;
            const doc = data.assigned_doctor || {};
            const profile = data.doctor_profile || {};

            setDoctor({
                name: doc.doctorName || 'Doctor',
                gender: profile.gender || 'N/A',
                picture: profile.picture || '/default.png',
            });
            console.log(profile.picture);
            sessionStorage.setItem('authToken', token);
            sessionStorage.setItem('doctorName', doc.doctorName || 'Doctor');

            setTimeout(() => {
                window.open(`/meeting?authToken=${token}`, '_blank');
            }, 3000);
        } catch (error) {
            console.error('❌ Booking failed:', error);
            alert('Something went wrong while booking consultation.');
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <>
                <Navbar />
                <div
                    style={{
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100vh',
                        background: '#f4f8ff',
                        fontFamily: 'Arial',
                        width: '100vw',
                    }}
                >
                    {doctor.picture && (
                        <img
                            src={`/doctor_pics/${doctor.picture}`}
                            onError={(e) =>
                                (e.currentTarget.src = '/default.png')
                            }
                            alt="Doctor"
                            style={{
                                width: '120px',
                                borderRadius: '50%',
                                marginBottom: '20px',
                            }}
                        />
                    )}
                    <h2>Connecting you to Dr. {doctor.name}</h2>
                    <p style={{ marginBottom: '30px', color: '#666' }}>
                        Gender: {doctor.gender}
                    </p>
                    <div
                        style={{
                            width: '40px',
                            height: '40px',
                            border: '4px solid #ccc',
                            borderTop: '4px solid #007bff',
                            borderRadius: '50%',
                            animation: 'spin 0.5s linear infinite',
                        }}
                    />
                    <style>{`
                        @keyframes spin {
                            0% { transform: rotate(0deg); }
                            100% { transform: rotate(360deg); }
                        }
                    `}</style>
                </div>
                <Footer />
            </>
        );
    }

    return (
        <>
            <Navbar />
            <section
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                    padding: '20px 0',
                    background: 'linear-gradient(to right, #f9f9f9, #e8f0ff)',
                    minHeight: '100vh',
                    width: '100vw',
                }}
            >
                <h1 style={{ fontSize: '2.5rem', color: '#333' }}>
                    Start Your Consultation
                </h1>
                <label
                    htmlFor="symptom"
                    style={{
                        marginTop: '20px',
                        marginBottom: '8px',
                        fontSize: '1rem',
                        color: '#333',
                    }}
                >
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
