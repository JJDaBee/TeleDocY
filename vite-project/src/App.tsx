import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
    useNavigate,
} from 'react-router-dom';
import Home from './pages/Home';
import Consultation from './pages/Consultation';
import SymptomChecker from './pages/SymptomChecker';
import MeetingPage from './pages/MeetingPage';

function App() {
    return (
        <Router>
            <nav style={{ padding: '10px' }}>
                <Link to="/" style={{ marginRight: '10px' }}>
                    Home
                </Link>
                <Link to="/consultation" style={{ marginRight: '10px' }}>
                    Consultation
                </Link>
                <Link to="/symptom-checker">Symptom Checker</Link>
            </nav>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/consultation" element={<Consultation />} />
                <Route path="/symptom-checker" element={<SymptomChecker />} />
                <Route path="/meeting" element={<MeetingPage />} />
            </Routes>
        </Router>
    );
}

export default App;
