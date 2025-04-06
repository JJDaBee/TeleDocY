import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/navbar';
import Footer from '../components/footer';

// Types
interface MedicationRow {
    medication: string;
    dosage: string;
    quantity: number;
}

interface Consult {
    firstname: string;
    medicalhistory?: string;
    symptom: string;
    roomid: string;
    uuid?: string;
    nric?: string;
}

const Dashboard: React.FC = () => {
    const navigate = useNavigate();
    const storedUser = sessionStorage.getItem('loggedInUser');
    const doctorName = storedUser ? JSON.parse(storedUser).doctorName : '';

    const [consults, setConsults] = useState<Consult[]>([]);
    const [showPopup, setShowPopup] = useState(false);
    const [selectedConsult, setSelectedConsult] = useState<Consult | null>(
        null
    );
    const [form, setForm] = useState({
        patientID: '',
        nric: '',
        date: '',
        diagnosis: '',
    });
    const [medications, setMedications] = useState<MedicationRow[]>([
        { medication: '', dosage: '', quantity: 1 },
    ]);

    useEffect(() => {
        const fetchConsults = async () => {
            try {
                const encodedDoctorName = encodeURIComponent(doctorName);
                const res = await fetch(
                    `http://localhost:5008/consults/doctor/${encodedDoctorName}`
                );
                const data = await res.json();
                setConsults(data.data || []);
            } catch (err) {
                console.error('❌ Failed to fetch consults:', err);
            }
        };
        fetchConsults();
    }, [doctorName]);

    if (!doctorName) return <h2>Access denied. Please log in as a doctor.</h2>;

    const handleJoinRoom = async (roomid: string) => {
        try {
            const res = await fetch('http://localhost:5000/create-token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    participantName: doctorName,
                    meetingId: roomid,
                }),
            });
            const data = await res.json();
            window.open(`/meeting?authToken=${data.authToken}`, '_blank');
        } catch (err) {
            console.error('❌ Failed to join room:', err);
        }
    };

    const openPopup = (consult: Consult) => {
        setSelectedConsult(consult);
        setForm({
            patientID: consult.uuid || '',
            nric: consult.nric || '',
            date: '',
            diagnosis: '',
        });
        setShowPopup(true);
    };

    const closePopup = () => {
        setShowPopup(false);
        setForm({ patientID: '', nric: '', date: '', diagnosis: '' });
        setMedications([{ medication: '', dosage: '', quantity: 1 }]);
    };

    const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setForm((prev) => ({ ...prev, [name]: value }));
    };

    const handleMedChange = (
        index: number,
        field: keyof MedicationRow,
        value: string | number
    ) => {
        const updated = [...medications];
        (updated[index] as any)[field] =
            field === 'quantity' ? parseInt(value as string, 10) : value;
        setMedications(updated);
    };

    const addMedicationRow = () => {
        setMedications([
            ...medications,
            { medication: '', dosage: '', quantity: 1 },
        ]);
    };

    const handleSubmit = async () => {
        if (!selectedConsult || !form.diagnosis.trim()) {
            alert('Please fill in the diagnosis.');
            return;
        }

        const payload = {
            uuid: selectedConsult.uuid, // taken from the selected consult
            reasonForVisit: selectedConsult.symptom, // taken from consult's symptom
            doctorname: doctorName,
            diagnosis: form.diagnosis,
            prescriptions: medications.map((m) => ({
                medicineName: m.medication,
                dosage: m.dosage,
                quantity: m.quantity,
            })),
        };
        console.log('📦 Payload to submit:', payload);

        try {
            const response = await fetch('http://localhost:5200/settle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            const result = await response.json();
            if (response.ok) {
                console.log('✅ Prescription submitted:', result);
                closePopup();
            } else {
                console.error('❌ Error submitting prescription:', result);
                alert('⚠️ Failed to submit prescription.');
            }
        } catch (error) {
            console.error('❌ Network error:', error);
            alert('❌ Network error while submitting.');
        }
    };

    return (
        <>
            <Navbar />
            <section
                style={{
                    padding: '60px',
                    background: 'linear-gradient(to right, #f9f9f9, #e8f0ff)',
                    minHeight: '100vh',
                    width: '100vw',
                }}
            >
                <div
                    style={{ width: '90%', maxWidth: '1000px', margin: 'auto' }}
                >
                    <h2
                        style={{
                            fontSize: '2rem',
                            marginBottom: '30px',
                            color: '#333',
                        }}
                    >
                        Consults
                    </h2>

                    <div
                        style={{
                            fontWeight: 'bold',
                            display: 'flex',
                            justifyContent: 'space-between',
                            marginBottom: '10px',
                            color: 'black',
                        }}
                    >
                        <span>Patient</span>
                        <span>Medical History</span>
                        <span>Symptoms</span>
                        <span>Actions</span>
                    </div>

                    {consults.map((consult, idx) => (
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
                            <div>
                                <strong>{consult.firstname}</strong>
                            </div>
                            <div>
                                {consult.medicalhistory || (
                                    <i style={{ color: '#777' }}>None</i>
                                )}
                            </div>
                            <div>{consult.symptom}</div>
                            <div
                                style={{
                                    display: 'flex',
                                    flexDirection: 'column',
                                    gap: '10px',
                                }}
                            >
                                <button
                                    onClick={() =>
                                        handleJoinRoom(consult.roomid)
                                    }
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
                                    onClick={() => openPopup(consult)}
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
                                zIndex: 1000,
                            }}
                        >
                            <div
                                style={{
                                    backgroundColor: 'white',
                                    padding: 30,
                                    borderRadius: 12,
                                    width: '100%',
                                    maxWidth: 700,
                                    maxHeight: '90vh',
                                    overflowY: 'auto',
                                }}
                            >
                                <h3
                                    style={{
                                        color: '#333',
                                        textAlign: 'center',
                                        marginBottom: '20px',
                                    }}
                                >
                                    Create Prescription for{' '}
                                    {selectedConsult?.firstname}
                                </h3>
                                <input
                                    name="diagnosis"
                                    placeholder="Diagnosis"
                                    type="text"
                                    onChange={handleFormChange}
                                    value={form.diagnosis}
                                    style={inputStyle}
                                />
                                <hr style={{ margin: '20px 0' }} />
                                <h4 style={{ marginBottom: '10px' }}>
                                    Medications
                                </h4>
                                <table
                                    style={{
                                        width: '100%',
                                        marginBottom: '20px',
                                        borderCollapse: 'collapse',
                                    }}
                                >
                                    <thead>
                                        <tr>
                                            <th style={tableHeaderStyle}>
                                                Medication
                                            </th>
                                            <th style={tableHeaderStyle}>
                                                Quantity
                                            </th>
                                            <th style={tableHeaderStyle}>
                                                Dosage
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {medications.map((med, i) => (
                                            <tr key={i}>
                                                <td>
                                                    <input
                                                        value={med.medication}
                                                        onChange={(e) =>
                                                            handleMedChange(
                                                                i,
                                                                'medication',
                                                                e.target.value
                                                            )
                                                        }
                                                        style={inputStyle}
                                                    />
                                                </td>
                                                <td>
                                                    <input
                                                        type="number"
                                                        value={med.quantity}
                                                        onChange={(e) =>
                                                            handleMedChange(
                                                                i,
                                                                'quantity',
                                                                e.target.value
                                                            )
                                                        }
                                                        style={inputStyle}
                                                    />
                                                </td>
                                                <td>
                                                    <input
                                                        value={med.dosage}
                                                        onChange={(e) =>
                                                            handleMedChange(
                                                                i,
                                                                'dosage',
                                                                e.target.value
                                                            )
                                                        }
                                                        style={inputStyle}
                                                    />
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                                <button
                                    onClick={addMedicationRow}
                                    style={{ marginBottom: '20px' }}
                                >
                                    ➕ Add Medication
                                </button>
                                <div
                                    style={{
                                        display: 'flex',
                                        justifyContent: 'flex-end',
                                        gap: '10px',
                                    }}
                                >
                                    <button onClick={handleSubmit}>
                                        Submit
                                    </button>
                                    <button onClick={closePopup}>Cancel</button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
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
