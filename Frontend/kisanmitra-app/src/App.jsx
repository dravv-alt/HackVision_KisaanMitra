import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import FarmManagement from './pages/FarmManagement';
import PlanningStage from './pages/PlanningStage';
import FarmingStage from './pages/FarmingStage';
import PostHarvestStage from './pages/PostHarvestStage';
import CollaborativeFarming from './pages/CollaborativeFarming';
import Inventory from './pages/Inventory';
import GovernmentSchemes from './pages/GovernmentSchemes';

import Finance from './pages/Finance';

import ActiveCrops from './pages/ActiveCrops';
import PriorityAlerts from './pages/PriorityAlerts';
import FarmingCalendarPage from './pages/FarmingCalendarPage';

// Placeholder components for other routes
const Placeholder = ({ title }) => (
  <div className="card">
    <h2>{title}</h2>
    <p>Coming Soon...</p>
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="active-crops" element={<ActiveCrops />} />
          <Route path="alerts" element={<PriorityAlerts />} />
          <Route path="farm-management" element={<FarmManagement />} />
          <Route path="farm-management/planning" element={<PlanningStage />} />
          <Route path="farm-management/farming" element={<FarmingStage />} />
          <Route path="farm-management/post-harvest" element={<PostHarvestStage />} />
          <Route path="collaborative" element={<CollaborativeFarming />} />
          <Route path="inventory" element={<Inventory />} />
          <Route path="finance" element={<Finance />} />
          <Route path="schemes" element={<GovernmentSchemes />} />
          <Route path="farm-management/calendar" element={<FarmingCalendarPage />} />

          {/* Catch-all redirect to Home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
