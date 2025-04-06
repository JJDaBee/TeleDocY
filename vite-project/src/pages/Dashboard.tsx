import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/navbar';
import Footer from '../components/footer';

// 🧾 Types

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

type MedicationRow = {
    medication: string;
    dosage: string;
    quantity: number;
};

// 📄 Mock consultations
const sampleConsultations: Consultation[] = [
    { patientName: 'John Doe', userInput: 'Headache and nausea' },
    { patientName: 'Jane Smith', userInput: 'Fever and cough' },
];

const doctorName = 'Dr. Alice';

const Dashboard: React.FC<DashboardProps> = ({ user }) => {
    const navigate = useNavigate();
    const [showPopup, setShowPopup] = useState(false);
    const [selectedPatient, setSelectedPatient] = useState<string | null>(null);
    const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
    const [historyMap, setHistoryMap] = useState<Record<string, any[]>>({});


    const [form, setForm] = useState({
        patientID: '',
        nric: '',
        date: '',
        diagnosis: '', // ✅ Added

    });

    const [medications, setMedications] = useState<MedicationRow[]>([
        { medication: '', dosage: '', quantity: 1 },
    ]);

    if (!user || user.role !== 'doctor') {
        return <h2>Access denied</h2>;
    }

    const openPopup = (patientName: string) => {
        setSelectedPatient(patientName);
        setShowPopup(true);
    };

    const closePopup = () => {
        setShowPopup(false);
        setForm({ patientID: '', nric: '', date: '', diagnosis: '' });
        setMedications([{ medication: '', dosage: '', quantity: 1 }]);
    };

    const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setForm(prev => ({ ...prev, [name]: value }));
    };

    const handleMedChange = (index: number, field: keyof MedicationRow, value: string | number) => {
        const updated = [...medications];
        (updated[index] as any)[field] = field === 'quantity' ? Number(value) : value;
        setMedications(updated);
    };

    const addMedicationRow = () => {
        setMedications([...medications, { medication: '', dosage: '', quantity: 1 }]);
    };



    //PATIENT HISTORY MEDICAL
    const toggleHistory = async (idx: number, patientName: string) => {
        if (expandedIndex === idx) {
            setExpandedIndex(null); // collapse
        } else {
            if (!historyMap[patientName]) {
                try {
                    const res = await fetch(`http://host.docker.internal:5008/consultation-history/${patientName}`);
                    const data = await res.json();
                    setHistoryMap(prev => ({ ...prev, [patientName]: data.data }));
                } catch (err) {
                    console.error('❌ Failed to fetch history:', err);
                    setHistoryMap(prev => ({ ...prev, [patientName]: [] }));
                }
            }
            setExpandedIndex(idx); // expand
        }
    };



    const handleSubmit = async () => {
        const payload = {
            uuid: form.patientID,
            nric: form.nric,
            dateTime: new Date().toISOString(), // or use form.date if needed
            reasonForVisit: selectedPatient || 'General Consultation', //take from gpt; KIV might delete
            doctorName: doctorName,
            diagnosis: form.diagnosis,
            prescriptions: medications.map(m => `${m.medication} ${m.dosage} x${m.quantity}`).join(', ')
        };

        console.log('📤 Submitting to post-consult composite service:', payload);

        try {
            const response = await fetch('http://host.docker.internal:5200/post-consult', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                alert('✅ Composite POST to post-consult successful!');
                closePopup();
            } else {
                const err = await response.json();
                console.error('❌ Error from post-consult:', err);
                alert('⚠️ Failed to submit composite POST.');
            }
        } catch (error) {
            console.error('❌ Network error posting to post-consult:', error);
            alert('❌ Failed to connect to post-consult service.');
        }
    };


    return (
        <>
            <Navbar />
            <section
                style={{
                    padding: '60px 60px',
                    background: 'linear-gradient(to right, #f9f9f9, #e8f0ff)',
                    minHeight: '100vh',
                    width: '100vw'

                }}
            >
                <div style={{ width: '900px', margin: 'auto' }}>
                    <h2 style={{ fontSize: '2rem', marginBottom: '30px', color: '#333' }}>
                        Consultation History
                    </h2>

                    {/* 🆕 Optional: Add header for better accessibility */}
                    <div style={{ fontWeight: 'bold', display: 'flex', justifyContent: 'space-between', marginBottom: '10px', color: 'black' ,width: '90vw'}}>
                        <span>Patient</span>
                        <span>Medical History</span>
                        <span>Symptoms</span>
                        <span>Actions</span>
                    </div>
                    </div>

                    {sampleConsultations.map((consult, idx) => (
                        <div
                            key={idx}
                            style={{
                                display: 'grid',
                                gridTemplateColumns: '1fr 2fr 1fr 1fr',
                                alignItems: 'start',
                                borderBottom: '2px solid black',
                                padding: '10px 0',
                                color: 'black',
                            }}
                        >
                            <div><strong>{consult.patientName}</strong></div>

                            {/* Always-shown history column */}
                            <div style={{ paddingRight: '10px' }}>
                                {historyMap[consult.patientName]?.length > 0 ? (
                                    <ul style={{ paddingLeft: '20px', margin: 0 }}>
                                        {historyMap[consult.patientName].map((entry, i) => (
                                            <li key={i} style={{ marginBottom: '8px' }}>
                                                <strong>Date:</strong> {entry.datetime}<br />
                                                <strong>Diagnosis:</strong> {entry.diagnosis}<br />
                                                <strong>Prescription:</strong> {entry.prescriptions}
                                            </li>
                                        ))}
                                    </ul>
                                ) : (
                                    <p style={{ fontStyle: 'italic', color: '#777' }}>No history</p>
                                )}
                            </div>

                            <div>{consult.userInput}</div>

                            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                                <button
                                    onClick={async () => {
                                        const res = await fetch('http://localhost:5000/create-token', {
                                            method: 'POST',
                                            headers: { 'Content-Type': 'application/json' },
                                            body: JSON.stringify({ participantName: doctorName }),
                                        });
                                        const data = await res.json();
                                        window.open(`/meeting?authToken=${data.authToken}`, '_blank');
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


                    {showPopup && (
                        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
                            <div style={{ backgroundColor: 'white', padding: 30, borderRadius: 12, width: '100%', maxWidth: 700, maxHeight: '90vh', overflowY: 'auto' }}>
                                <h3 style={{ color: '#333', textAlign: 'center', marginBottom: '20px' }}>
                                    Create Prescription for {selectedPatient}
                                </h3>

                                <input name="patientID" placeholder="Patient ID" onChange={handleFormChange} value={form.patientID} style={inputStyle} />
                                <input name="nric" placeholder="NRIC" onChange={handleFormChange} value={form.nric} style={inputStyle} />
                                <input name="date" type="date" onChange={handleFormChange} value={form.date} style={inputStyle} />
                                <input name="diagnosis" placeholder="Diagnosis" type="text" onChange={handleFormChange} value={form.diagnosis} style={inputStyle} />

                                <hr style={{ margin: '20px 0' }} />

                                <h4 style={{ marginBottom: '10px' }}>Medications</h4>
                                <table style={{ width: '100%', marginBottom: '20px', borderCollapse: 'collapse' }}>
                                    <thead>
                                        <tr>
                                            <th style={tableHeaderStyle}>Medication</th>
                                            <th style={tableHeaderStyle}>Quantity</th>
                                            <th style={tableHeaderStyle}>Dosage</th>

                                        </tr>
                                    </thead>
                                    <tbody>
                                        {medications.map((med, i) => (
                                            <tr key={i}>
                                                <td><input value={med.medication} onChange={e => handleMedChange(i, 'medication', e.target.value)} style={inputStyle} /></td>
                                                <td><input type="number" value={med.quantity} onChange={e => handleMedChange(i, 'quantity', e.target.value)} style={inputStyle} /></td>
                                                <td><input value={med.dosage} onChange={e => handleMedChange(i, 'dosage', e.target.value)} style={inputStyle} /></td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>

                                <button onClick={addMedicationRow} style={{ marginBottom: '20px' }}>➕ Add Medication</button>

                                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
                                    <button onClick={handleSubmit}>Submit</button>
                                    <button onClick={closePopup}>Cancel</button>
                                </div>
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
    padding: '10px',
    borderRadius: '6px',
    border: '1px solid #ccc',
    fontSize: '1rem',
    boxSizing: 'border-box',
};

const tableHeaderStyle: React.CSSProperties = {
    textAlign: 'left',
    paddingBottom: '8px',
    color: 'black',
    borderBottom: '1px solid #ccc',
};

export default Dashboard;
