import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import SearchDashboard from './pages/SearchDashboard';

import AnalyticsDashboard from './pages/AnalyticsDashboard';
import BriefingsDashboard from './pages/BriefingsDashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        {/* All internal authenticated/dashboard routes could go here */}
        <Route path="/dashboard" element={<SearchDashboard />} />
        <Route path="/analytics" element={<AnalyticsDashboard />} />
        <Route path="/analytics/:creatorId" element={<AnalyticsDashboard />} />
        <Route path="/briefings" element={<BriefingsDashboard />} />
        <Route path="/briefings/:creatorId" element={<BriefingsDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
