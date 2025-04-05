import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/navbar';
import Footer from '../components/footer';

type User = {
    username: string;
    password: string;
    role: 'patient' | 'doctor';
};

type DashboardProps = {
    user: User | null;
};

type Consultation = {
    patientName: string;
    userInput: string;
};

const sampleConsultations: Consultation[] = [
    { patientName: 'John Doe', userInput: 'Headache and nausea' },
    { patientName: 'Jane Smith', userInput: 'Fever and cough' },
]; // Change this to take input from user context, etc.

const doctorName = 'Dr. Alice'; // Change this to take input from user context, etc.

const Dashboard: React.FC<DashboardProps> = ({ user }) => {
    const navigate = useNavigate();
    const [showPopup, setShowPopup] = useState(false);
    const [selectedPatient, setSelectedPatient] = useState<string | null>(null);

    const [form, setForm] = useState({
        patientID: '',
        nric: '',
        medication: '',
        dosage: '',
        pills: '',
        date: '',
    });

    if (!user || user.role !== 'doctor') {
        return <h2>Access denied</h2>;
    }

    const openPopup = (patientName: string) => {
        setSelectedPatient(patientName);
        setShowPopup(true);
    };

    const closePopup = () => {
        setShowPopup(false);
        setForm({
            patientID: '',
            nric: '',
            medication: '',
            dosage: '',
            pills: '',
            date: '',
        });
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setForm((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = () => {
        console.log('Prescription Order:', {
            ...form,
            patientName: selectedPatient,
        });
        closePopup();
    };

    return (
        <>
            <Navbar />
            <section
                style={{
                    padding: '60px 20px',
                    background: 'linear-gradient(to right, #f9f9f9, #e8f0ff)', // ✨ Gradient background
                    minHeight: '100vh',
                    boxSizing: 'border-box',
                    minWidth: '100vw'
                }}
            >
                <div style={{ maxWidth: '900px', margin: 'auto' }}>
                    <h2 style={{ fontSize: '2rem', marginBottom: '30px', color: '#333' }}>
                        Consultation History
                    </h2>

                    {sampleConsultations.map((consult, idx) => (
                        <div
                            key={idx}
                            style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                borderBottom: '2px solid black',
                                padding: '10px 0',
                            }}
                        >
                            <div>
                                <strong>{consult.patientName}</strong> &nbsp;&nbsp;
                                {consult.userInput}
                            </div>
                            <div
                                style={{
                                    display: 'flex',
                                    flexDirection: 'column',
                                    gap: '10px',
                                }}
                            >
                                <button
                                    onClick={async () => {
                                        const participantName = doctorName;
                                        try {
                                            const res = await fetch('http://localhost:5000/create-token', {
                                                method: 'POST',
                                                headers: { 'Content-Type': 'application/json' },
                                                body: JSON.stringify({ participantName }),
                                            });

                                            let authToken = '';
                                            if (res.ok) {
                                                const data = await res.json();
                                                authToken = data.authToken;
                                                console.log('Received token from backend:', authToken);
                                            }

                                            const meetingURL = `/meeting?authToken=${authToken}`;
                                            window.open(meetingURL, '_blank');
                                        } catch (error) {
                                            console.error('Error fetching token:', error);
                                            alert('Unable to join the consultation. Please try again.');
                                        }
                                    }}
                                    style={{
                                        backgroundColor: 'red',
                                        color: 'white',
                                        padding: '8px 12px',
                                        borderRadius: '20px',
                                        border: 'none',
                                    }}
                                >
                                    Join Room
                                </button>

                                <button
                                    onClick={() => openPopup(consult.patientName)}
                                    style={{
                                        backgroundColor: 'red',
                                        color: 'white',
                                        padding: '8px 12px',
                                        borderRadius: '20px',
                                        border: 'none',
                                    }}
                                >
                                    Create Order
                                </button>
                            </div>
                        </div>
                    ))}
                </div>


                {/* Popup */}
                {showPopup && (
                    <div
                        style={{
                            position: 'fixed',
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            backgroundColor: 'rgba(0,0,0,0.5)',
                            display: 'flex',
                            justifyContent: 'center',
                            alignItems: 'center',
                        }}
                    >
                        <div
                            style={{
                                backgroundColor: 'white',
                                padding: '30px',
                                borderRadius: '12px', // 🔧 Rounded card style
                                width: '100%',
                                maxWidth: '420px',
                                boxShadow: '0 4px 20px rgba(0,0,0,0.2)', // 🔧 Soft shadow
                            }}
                        >
                            <h3>Create Prescription for {selectedPatient}</h3>
                            <input
                                name="patientID"
                                placeholder="Patient ID"
                                onChange={handleChange}
                                value={form.patientID}
                                style={inputStyle}

                            />
                            <br />
                            <br />
                            <input
                                name="nric"
                                placeholder="NRIC"
                                onChange={handleChange}
                                value={form.nric}
                                style={inputStyle}

                            />
                            <br />
                            <br />
                            <input
                                name="medication"
                                placeholder="Medication"
                                onChange={handleChange}
                                value={form.medication}
                                style={inputStyle}

                            />
                            <br />
                            <br />
                            <input
                                name="dosage"
                                placeholder="Dosage"
                                onChange={handleChange}
                                value={form.dosage}
                                style={inputStyle}

                            />
                            <br />
                            <br />
                            <input
                                name="pills"
                                placeholder="Number of Pills"
                                onChange={handleChange}
                                value={form.pills}
                                style={inputStyle}

                            />
                            <br />
                            <br />
                            <input
                                name="date"
                                placeholder="Prescription Date"
                                type="date"
                                onChange={handleChange}
                                value={form.date}
                                style= {inputStyle}
                            />
                            <br />
                            <br />
                            <button onClick={handleSubmit}>Submit</button>
                            <button
                                onClick={closePopup}
                                style={{ marginLeft: '10px' }}
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                )}
            </section>
            <Footer />
            </>


            );
};

const inputStyle: React.CSSProperties = {
    width: '100%',
    padding: '12px',
    margin: '10px 0',
    border: '1px solid #ccc',
    borderRadius: '8px',
    fontSize: '1rem',
};
            export default Dashboard;
