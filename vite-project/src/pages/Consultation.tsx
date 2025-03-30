import { useNavigate } from 'react-router-dom';

const Consultation = () => {
    const navigate = useNavigate();

    const handleConsult = () => {
        const sampleToken =
            'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmdJZCI6Ijc2NDVlM2E3LWY0N2MtNDJjNy1iNWM3LTI3NjA1NDk2OGY4OCIsIm1lZXRpbmdJZCI6ImJiYmIzMWE5LTkzZWUtNDIwYi04OWU0LWRkODUwMzI3MTU1NCIsInBhcnRpY2lwYW50SWQiOiJhYWFlZTU2NS0wNTUwLTQ3MzMtOWEwNi02ZWMyMjEyOThhNTIiLCJwcmVzZXRJZCI6ImE5MjI4MWFmLTAyMTQtNGNhNS1iOGJkLTA2ZmVjZWE0NWQyMSIsImlhdCI6MTc0MzMwOTcyMSwiZXhwIjoxNzUxOTQ5NzIxfQ.GopuNLhzIWdjGYZbHGePZ9NZLVLMeXY3jLcPS9z-lO-m-NtM-WrwYsQr_kB2k55LirVZCPUjW3EpOf5fjdcvvqjMjwwFAmdgGE3-iwHa7A4B-lbu98Ap-9MT_zZ-E7cgLOWIPAPcbrVY2XA8fhJ_gdNb2H5UlJwZX2CcgmYrUYogWjx5rW6-Cg6vBn6NZASOTHR8xAYlNsrsmNXSugYG7s6Tq4GwOlwo-_goBI6GmQSksBYcfLJLJBOcc21nSL9Ltsx_P7D9CIGsohmL74lqSMSMuF3mvE4DtJXUWpLgNKI7oYiUTPUAUnhOtgN2RtzrE0NIjtAcRrw2QrmcYnVYaw'; // Replace this or fetch dynamically
        navigate(`/meeting?authToken=${sampleToken}`);
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Consultation</h1>
            <button
                onClick={handleConsult}
                style={{ padding: '10px 20px', marginTop: '10px' }}
            >
                Consult
            </button>
        </div>
    );
};

export default Consultation;
