import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import {
  Dashboard,
  NewCampaignForm,
  ProspectExplorer,
  SequenceBuilder,
  ResponseDashboard,
} from './components/CampaignFeatures';


function App() {
  return (
    <BrowserRouter>
      <div style={{ fontFamily: 'sans-serif', background: '#f7f7fa', minHeight: '100vh' }}>
        <Navbar />
        <div style={{ maxWidth: 900, margin: '0 auto', padding: 24 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/new-campaign" element={<NewCampaignForm />} />
            <Route path="/prospects" element={<ProspectExplorer />} />
            <Route path="/sequence" element={<SequenceBuilder />} />
            <Route path="/responses" element={<ResponseDashboard />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

createRoot(document.getElementById('root')!).render(<App />);


