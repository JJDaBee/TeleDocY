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

    return <DyteMeeting meeting={meeting!} />;
}

export default MeetingPage;
