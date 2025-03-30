import { useState } from 'react';

const SymptomChecker = () => {
    const [symptom, setSymptom] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        alert(`You submitted: ${symptom}`);
        // You can integrate symptom analysis or AI here
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Symptom Checker</h1>
            <form onSubmit={handleSubmit}>
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
                >
                    Submit
                </button>
            </form>
        </div>
    );
};

export default SymptomChecker;
