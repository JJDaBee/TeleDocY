// import { StrictMode } from 'react'
// import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';
import ReactDOM from 'react-dom/client';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    // NOTE: Not using StrictMode to avoid the double execution of useEffect
    // while trying out the sample
    <App />
);
// createRoot(document.getElementById('root')!).render(
//     <StrictMode>
//         <App />
//     </StrictMode>
// );
