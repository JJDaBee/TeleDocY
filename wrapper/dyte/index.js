// === Backend: Express server to generate Dyte authToken for existing meetings ===

const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const DYTE_API_KEY = process.env.DYTE_API_KEY;
const DYTE_BASE_URL = 'https://api.dyte.io/v2';
const DYTE_MEETING_ID = process.env.DYTE_MEETING_ID;
const patientUuid = 'UUID-1234';

app.post('/create-token', async (req, res) => {
    try {
        const { participantName } = req.body;

        if (!DYTE_MEETING_ID || !participantName) {
            return res
                .status(400)
                .json({ error: 'meetingId and participantName are required' });
        }

        // Add participant to existing meeting
        const participantResponse = await axios.post(
            `${DYTE_BASE_URL}/meetings/${DYTE_MEETING_ID}/participants`,
            {
                name: participantName,
                preset_name: 'Test v1', // Or your custom preset
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
        // console.log('Participant added:', participantResponse);
        // console.log('Auth Token:', authToken);

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
    console.log(`🚀 Backend running on http://localhost:${PORT}`)
);
