const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
app.use(express.json());
app.use(cors());

// Orchestration function that calls the external API
async function fetchPatientDetails(nric) {
    const externalResponse = await axios.post(
        'https://personal-gbst4bsa.outsystemscloud.com/TeleDocY/rest/v1/GetPatientDetails',
        { nric }
    );
    return externalResponse.data;
}

// Composite endpoint that orchestrates the workflow
app.post('/api/consultation', async (req, res) => {
    const { symptoms, nric } = req.body;
    if (!nric) {
        return res.status(400).json({ error: 'NRIC is required' });
    }

    console.log(
        `Received consultation request for ${nric} with symptoms: ${symptoms}`
    );

    try {
        console.log('Calling external API for patient details...');
        // Orchestrate: call the function that gets patient details
        const patientDetails = await fetchPatientDetails(nric);
        console.log('External API response:', patientDetails);

        // Return a composed response with consultation acknowledgment and patient details
        res.json({
            message: 'Your consultation request has been received.',
            symptoms,
            nric,
            patientDetails,
        });
    } catch (error) {
        console.error('Error during orchestration:', error.message);
        res.status(500).json({ error: 'Failed to retrieve patient details' });
    }
});

app.listen(4000, '0.0.0.0', () =>
    console.log('API Gateway running on port 4000')
);
