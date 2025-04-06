// === Backend: Express server to generate Dyte authToken for existing meetings ===

const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const DYTE_API_KEY = process.env.DYTE_API_KEY;
const DYTE_BASE_URL = 'https://api.dyte.io/v2';
const patientUuid = 'UUID-1234'; // Optional: this can be dynamic if needed

app.post('/create-token', async (req, res) => {
    try {
        const { participantName, meetingId } = req.body;

        if (!participantName || !meetingId) {
            return res
                .status(400)
                .json({ error: 'meetingId and participantName are required' });
        }

        const participantResponse = await axios.post(
            `${DYTE_BASE_URL}/meetings/${meetingId}/participants`,
            {
                name: participantName,
                preset_name: 'Test v1',
                client_specific_id: patientUuid,
            },
            {
                headers: {
                    Authorization: `Basic ${DYTE_API_KEY}`,
                    'Content-Type': 'application/json',
                },
            }
        );

        const authToken = participantResponse.data.data.token;
        res.json({ authToken });
    } catch (error) {
        console.error(
            'Error creating token:',
            error.response?.data || error.message
        );
        res.status(500).json({ error: 'Failed to create token' });
    }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () =>
    console.log(`🚀 Dyte wrapper running on http://localhost:${PORT}`)
);
