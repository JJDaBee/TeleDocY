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
        <div style={{ padding: '20px' }}>
            <h1>Symptom Checker</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Enter patient UUID..."
                    value={uuid}
                    onChange={(e) => setUuid(e.target.value)}
                    style={{ padding: '10px', width: '300px', marginBottom: '10px', display: 'block' }}
                />
                <input
                    type="text"
                    placeholder="Describe your symptoms..."
                    value={symptom}
                    onChange={(e) => setSymptom(e.target.value)}
                    style={{ padding: '10px', width: '300px' }}
                />
                <button
                    type="submit"
                    style={{ padding: '10px 20px', marginLeft: '10px' }}
                    disabled={loading}
                >
                    {loading ? 'Checking...' : 'Submit'}
                </button>
            </form>

            {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}

            {result && (
                <div style={{ marginTop: '20px' }}>
                    <h3>AI Response:</h3>
                    <p>{result.ai_response}</p>

                    <h4>Patient Info:</h4>
                    <pre>{JSON.stringify(result.patient_info, null, 2)}</pre>

                    <h4>Consultation History:</h4>
                    <pre>{JSON.stringify(result.consultation_history, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default SymptomChecker;
