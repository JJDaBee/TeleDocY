import { useState } from 'react';
import axios from 'axios';

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
            const response = await axios.post('http://localhost:8000/check-symptoms', {
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
        <div style={{ padding: '40px', maxWidth: '700px', margin: '0 auto', fontFamily: 'Arial, sans-serif' }}>
            <h1 style={{ marginBottom: '30px', textAlign: 'center' }}>Symptom Checker</h1>

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <input
                    type="text"
                    placeholder="Enter patient UUID..."
                    value={uuid}
                    onChange={(e) => setUuid(e.target.value)}
                    style={{
                        padding: '12px',
                        fontSize: '16px',
                        borderRadius: '5px',
                        border: '1px solid #ccc',
                    }}
                />
                <input
                    type="text"
                    placeholder="Describe your symptoms..."
                    value={symptom}
                    onChange={(e) => setSymptom(e.target.value)}
                    style={{
                        padding: '12px',
                        fontSize: '16px',
                        borderRadius: '5px',
                        border: '1px solid #ccc',
                    }}
                />
                <button
                    type="submit"
                    disabled={loading}
                    style={{
                        padding: '12px',
                        fontSize: '16px',
                        borderRadius: '5px',
                        backgroundColor: '#007bff',
                        color: '#fff',
                        border: 'none',
                        cursor: 'pointer',
                    }}
                >
                    {loading ? 'Checking...' : 'Submit'}
                </button>
            </form>

            {error && (
                <p style={{ color: 'red', marginTop: '20px', textAlign: 'center' }}>{error}</p>
            )}

            {result && (
                <div style={{ marginTop: '30px' }}>
                    <div style={{ background: '#f9f9f9', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
                        <h3>AI Response:</h3>
                        <p>{result.ai_response}</p>
                    </div>

                    <div style={{ background: '#f1f1f1', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
                        <h4>Patient Info:</h4>
                        <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(result.patient_info, null, 2)}</pre>
                    </div>

                    <div style={{ background: '#f1f1f1', padding: '20px', borderRadius: '8px' }}>
                        <h4>Consultation History:</h4>
                        <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(result.consultation_history, null, 2)}</pre>
                    </div>
                </div>
            )}
        </div>
    );
};

export default SymptomChecker;
