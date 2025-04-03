// src/App.tsx
import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Consultation from './pages/Consultation';
import SymptomChecker from './pages/SymptomChecker';
import MeetingPage from './pages/MeetingPage';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';

type User = {
    username: string;
    password: string;
    role: 'patient' | 'doctor';
};

function App() {
    const [user, setUser] = useState<User | null>(null);

    return (
        <Router>
            <nav style={{ padding: '10px' }}>
                <Link to="/" style={{ marginRight: '10px' }}>
                    Home
                </Link>
                <Link to="/consultation" style={{ marginRight: '10px' }}>
                    Consultation
                </Link>
                <Link to="/symptom-checker" style={{ marginRight: '10px' }}>
                    Symptom Checker
                </Link>
                <Link to="/login" style={{ marginRight: '10px' }}>
                    Login
                </Link>
                {user?.role === 'doctor' && (
                    <Link to="/dashboard">Dashboard</Link>
                )}
            </nav>
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
            </Routes>
        </Router>
    );
}

export default App;
