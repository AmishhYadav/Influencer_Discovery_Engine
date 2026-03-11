import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import SearchDashboard from './pages/SearchDashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        {/* All internal authenticated/dashboard routes could go here */}
        <Route path="/dashboard" element={<SearchDashboard />} />
        <Route path="/analytics" element={<SearchDashboard />} />
        <Route path="/briefings" element={<SearchDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
