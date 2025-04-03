// import React from 'react';

const Consultation = () => {
    const handleConsult = async () => {
        // const meetingId = 'your_precreated_meeting_id'; // Replace with actual meeting ID
        const participantName = 'Alice'; // This can come from user context, input, etc.

        try {
            const res = await fetch('http://localhost:5000/create-token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ participantName }),
            });
            if (!res.ok) {
                throw new Error('Failed to create token');
            }

            const { authToken } = await res.json();

            // Open Dyte meeting page in a new tab
            const meetingURL = `/meeting?authToken=${authToken}`;
            window.open(meetingURL, '_blank');
        } catch (error) {
            console.error('❌ Error fetching token:', error);
            alert('Unable to join the consultation. Please try again.');
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Consultation</h1>
            <button
                onClick={handleConsult}
                style={{ padding: '10px 20px', marginTop: '10px' }}
            >
                Join Consultation
            </button>
        </div>
    );
};

export default Consultation;
