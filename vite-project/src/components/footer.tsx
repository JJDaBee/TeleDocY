import React from 'react';

const Footer: React.FC = () => {
    return (
        <footer
            style={{
                textAlign: 'center',
                padding: '20px',
                backgroundColor: '#f1f1f1',
                marginTop: 'auto',
            }}
        >
            <p style={{ margin: 0, color: '#666' }}>
                &copy; {new Date().getFullYear()} TeleDoc. All rights reserved.
            </p>
        </footer>
    );
};

export default Footer;
