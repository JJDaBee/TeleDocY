// src/pages/MeetingPage.tsx
import { useEffect } from 'react';
import { DyteMeeting } from '@dytesdk/react-ui-kit';
import { useDyteClient } from '@dytesdk/react-web-core';

function MeetingPage() {
    const [meeting, initMeeting] = useDyteClient();

    useEffect(() => {
        const searchParams = new URL(window.location.href).searchParams;
        const authToken = searchParams.get('authToken');

        if (!authToken) {
            alert('Missing authToken in URL.');
            return;
        }

        initMeeting({ authToken });
    }, []);

    // ✅ Redirect parent tab to /home if this tab closes
    useEffect(() => {
        const handleUnload = () => {
            if (window.opener && !window.opener.closed) {
                window.opener.location.href = '/';
            }
        };

        window.addEventListener('beforeunload', handleUnload);
        return () => window.removeEventListener('beforeunload', handleUnload);
    }, []);

    return meeting ? (
        <DyteMeeting meeting={meeting} />
    ) : (
        <p>Loading meeting...</p>
    );
}

export default MeetingPage;
