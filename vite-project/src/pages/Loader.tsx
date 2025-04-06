import React, { useEffect, useState } from 'react';
import Navbar from '../components/navbar';
import Footer from '../components/footer';

const Loader: React.FC = () => {
    const [doctor, setDoctor] = useState({ name: '', gender: '', picture: '' });

    useEffect(() => {
        const symptom = sessionStorage.getItem('symptom');
        const uuid = sessionStorage.getItem('uuid');

        const bookConsult = async () => {
            try {  //PLEASE DBL CONFIRM if not js do from scrath agn 
                const res = await fetch('http://localhost:5100/book_consult', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ uuid, reasonForVisit: symptom }),
                });

                const data = await res.json();
                const token = data.dyte_token;
                const doc = data.assigned_doctor || {};
                const doctor= data.doctor_profile || {}; //doctor is for doctorprofile 
                setDoctor({
                    name: doc.doctorName || 'Assigned Doctor',
                    gender: doctor.gender || 'N/A',
                    picture: doctor.picture || '/default.png',
                });

                sessionStorage.setItem('authToken', token);
                sessionStorage.setItem('doctorName', doc.doctorName || 'Doctor');

                setTimeout(() => {
                    window.location.href = `/meeting?authToken=${token}`;
                }, 5000);
            } catch (error) {
                console.error('❌ Booking failed:', error);
                alert('Something went wrong while booking consultation.');
            }
        };

        bookConsult();
    }, []);

    return (
        <>
            <Navbar />
            <div style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
                background: '#f4f8ff',
                fontFamily: 'Arial',
                width: '100vw',
            }}>
                <img
                    src={doctor.picture}
                    alt="Doctor"
                    style={{ width: '120px', borderRadius: '50%', marginBottom: '20px' }}
                />
                <h2>Connecting you to Dr. {doctor.name}</h2>
                <p style={{ marginBottom: '30px', color: '#666' }}>Gender: {doctor.gender}</p>
                <div style={{
                    width: '40px',
                    height: '40px',
                    border: '4px solid #ccc',
                    borderTop: '4px solid #007bff',
                    borderRadius: '50%',
                    animation: 'spin 0.5s linear infinite'
                }} />
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
};

export default Loader;
