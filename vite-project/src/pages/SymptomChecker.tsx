import { useState } from 'react';
import axios from 'axios';
import Navbar from '../components/navbar';
import Footer from '../components/footer';

const SymptomChecker = () => {
    const [uuid, setUuid] = useState('');
    const [symptom, setSymptom] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [result, setResult] = useState<any>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!uuid.trim() || !symptom.trim()) {
            setError('Please enter both UUID and symptom.');
            return;
        }

        setError('');
        setLoading(true);
        setResult(null);

        try {
            const response = await axios.post('http://localhost:4000/check-symptoms', {
                uuid,
                symptom_description: symptom,
            });
            setResult(response.data);
        } catch (err: any) {
            setError('Something went wrong. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <Navbar />
            <section
                style={{
                    padding: '60px 20px',
                    background: 'linear-gradient(to right, #f9f9f9, #e8f0ff)',
                    minHeight: '100vh',
                }}
            >
                <div style={{ minWidth: '100vw', maxWidth: '100vw', margin: 'auto' }}>
                    <h1 style={{ marginBottom: '30px', textAlign: 'center', fontSize: '2.5rem', color: '#333' }}>
                        🩺 Symptom Checker
                    </h1>

                    <form
                        onSubmit={handleSubmit}
                        style={{
                            backgroundColor: '#fff',
                            padding: '30px',
                            borderRadius: '10px',
                            boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '20px',
                            margin: '0 auto',
                            width: '80%',

                        }}
                    >
                        <input
                            type="text"
                            placeholder="Enter patient UUID..."
                            value={uuid}
                            onChange={(e) => setUuid(e.target.value)}
                            style={inputStyle}
                        />
                        <textarea
                            placeholder="Describe your symptoms..."
                            value={symptom}
                            onChange={(e) => setSymptom(e.target.value)}
                            rows={4}
                            style={{ ...inputStyle, resize: 'vertical' }}
                        />
                        <button
                            type="submit"
                            disabled={loading}
                            style={{
                                padding: '14px',
                                fontSize: '1rem',
                                borderRadius: '6px',
                                backgroundColor: '#007bff',
                                color: '#fff',
                                border: 'none',
                                cursor: 'pointer',
                                transition: 'background-color 0.3s',
                            }}
                        >
                            {loading ? 'Checking...' : 'Submit'}
                        </button>
                    </form>

                    {error && (
                        <p style={{ color: 'red', marginTop: '20px', textAlign: 'center' }}>{error}</p>
                    )}

                    {result && (
                        <div style={{ marginTop: '40px' }}>
                            <div style={cardStyle}>
                                <h3 style={cardTitle}>AI Response</h3>
                                <p>{result.ai_response}</p>
                            </div>

                            <div style={cardStyle}>
                                <h4 style={cardTitle}>Patient Info</h4>
                                <pre style={{ whiteSpace: 'pre-wrap', fontSize: '0.95rem' }}>
                                    {JSON.stringify(result.patient_info, null, 2)}
                                </pre>
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
    padding: '14px',
    fontSize: '1rem',
    borderRadius: '6px',
    border: '1px solid #ccc',
};

const cardStyle: React.CSSProperties = {
    background: '#007bff',
    padding: '20px',
    borderRadius: '10px',
    marginBottom: '25px',
    boxShadow: '0 2px 12px rgba(0,0,0,0.06)',
};

const cardTitle: React.CSSProperties = {
    marginBottom: '12px',
    fontSize: '1.2rem',
    color: '#333',
    fontWeight: 600,
};

export default SymptomChecker;
