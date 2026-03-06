import { Routes, Route } from 'react-router-dom'
import AppShell from '@/layout/AppShell'
import Dashboard from '@/pages/Dashboard'
import CreatorProfile from '@/pages/CreatorProfile'
import BriefingView from '@/pages/BriefingView'

function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/creator/:id" element={<CreatorProfile />} />
        <Route path="/briefing/:id" element={<BriefingView />} />
        <Route path="/briefings" element={<Dashboard />} />
      </Routes>
    </AppShell>
  )
}

export default App
