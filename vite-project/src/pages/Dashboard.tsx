import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

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
        <div style={{ padding: 20 }}>
            <h2>Consultation History</h2>
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
                                    // 🔄 Try to get a token from backend
                                    const res = await fetch('http://localhost:5000/create-token', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json',
                                        },
                                        body: JSON.stringify({ participantName }),
                                    });

                                    let authToken: string;

                                    if (res.ok) {
                                        const data = await res.json();
                                        authToken = data.authToken;
                                        console.log("Received token from backend:", authToken);
                                    } else {
                                        console.warn("Backend failed, using fallback token.");
                                        // ❗ HARDCODED TOKEN FOR TESTING
                                        authToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmdJZCI6Ijc2NDVlM2E3LWY0N2MtNDJjNy1iNWM3LTI3NjA1NDk2OGY4OCIsIm1lZXRpbmdJZCI6ImJiYjc4ZTVhLTQ0ZTUtNDc4OC1hY2M2LTdiNzc4NjM0NGIwOCIsInBhcnRpY2lwYW50SWQiOiJhYWFmZGNkMC1hNmJkLTRkODEtODVjOS1kNmJkN2U3OTFkYWUiLCJwcmVzZXRJZCI6ImE5MjI4MWFmLTAyMTQtNGNhNS1iOGJkLTA2ZmVjZWE0NWQyMSIsImlhdCI6MTc0MzYxNjYxNiwiZXhwIjoxNzUyMjU2NjE2fQ.uFKrflU8_Bee1p5CgMQB7KWy45chcI1-8lO0o37sef_p5VLDVK5-oTVPrr5AO5ZsvX2yVym2FKWx3G8WRgTcCl0017nzDQgw-kP1ssJAPpXo2V6zw4KFxR8Oq4Nh8QwOtCyEtZRFkrf9pRP_jop-V74PB0yN9hcwwTsQ2WuUnR6Xj73NfViY9pPm0EImrg5FFNula_rE4mkHa75R-YqSic_RFgCUzMgjRwjogBosRbw-GjUUE0acI0Dmk0gZ82QGRVDqgSAvWZgR1Lm6Dn3kC3DN_GVFrYgT7rRYasuNacUSFZJyw-AQMxbd_QPekB4CxXC9FooUb6eru8xPBJs7gw";
                                    }

                                    // Join Dyte meeting with token
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
                            padding: 30,
                            borderRadius: 8,
                            width: 400,
                        }}
                    >
                        <h3>Create Prescription for {selectedPatient}</h3>
                        <input
                            name="patientID"
                            placeholder="Patient ID"
                            onChange={handleChange}
                            value={form.patientID}
                        />
                        <br />
                        <br />
                        <input
                            name="nric"
                            placeholder="NRIC"
                            onChange={handleChange}
                            value={form.nric}
                        />
                        <br />
                        <br />
                        <input
                            name="medication"
                            placeholder="Medication"
                            onChange={handleChange}
                            value={form.medication}
                        />
                        <br />
                        <br />
                        <input
                            name="dosage"
                            placeholder="Dosage"
                            onChange={handleChange}
                            value={form.dosage}
                        />
                        <br />
                        <br />
                        <input
                            name="pills"
                            placeholder="Number of Pills"
                            onChange={handleChange}
                            value={form.pills}
                        />
                        <br />
                        <br />
                        <input
                            name="date"
                            placeholder="Prescription Date"
                            type="date"
                            onChange={handleChange}
                            value={form.date}
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
        </div>
    );
};

export default Dashboard;
