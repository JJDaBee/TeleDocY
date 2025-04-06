// src/App.tsx
import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Consultation from './pages/Consultation';
import SymptomChecker from './pages/SymptomChecker';
import MeetingPage from './pages/MeetingPage';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import Loader from './pages/Loader';
import Navbar from './components/navbar';
import Footer from './components/footer';
import { useEffect } from 'react';


type User = {
    username: string;
    password: string;
    role: 'patient' | 'doctor';
};

function App() {
    const [user, setUser] = useState<User | null>(null);
        useEffect(() => { //TO REDIRECT BACK TO HOME AFTER CALL
            const handleMessage = (event: MessageEvent) => {
                if (event.data?.type === 'MEETING_ENDED') {
                    console.log('📞 Meeting ended — redirecting to dashboard');
                    window.location.href = '/home'; 
                }
            };
    
            window.addEventListener('message', handleMessage);
            return () => window.removeEventListener('message', handleMessage);
        }, []);
    return (
        <Router>
          
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/consultation" element={<Consultation />} />
                <Route path="/symptom-checker" element={<SymptomChecker />} />
                <Route path="/meeting" element={<MeetingPage />} />
                <Route
                    path="/login"
                    element={<LoginPage setUser={setUser} />}
                />
                <Route path="/dashboard" element={<Dashboard user={user} />} />
                <Route path="/loader" element={<Loader />} />
            </Routes>
        </Router>
    );
}

export default App;
