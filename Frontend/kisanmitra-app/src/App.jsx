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

// Onboarding Pages
import Landing from './pages/Onboarding/Landing';
import Login from './pages/Onboarding/Login';
import LanguageSelection from './pages/Onboarding/LanguageSelection';
import LocationSetup from './pages/Onboarding/LocationSetup';
import SoilTypeSelection from './pages/Onboarding/SoilTypeSelection';
import FarmSizeInput from './pages/Onboarding/FarmSizeInput';
import CropSelection from './pages/Onboarding/CropSelection';
import OnboardingSummary from './pages/Onboarding/OnboardingSummary';

// Context
import { OnboardingProvider } from './context/OnboardingContext';
import { LanguageProvider } from './context/LanguageContext';
import OnboardingGuard from './components/OnboardingGuard';

// Placeholder components for other routes
const Placeholder = ({ title }) => (
  <div className="card">
    <h2>{title}</h2>
    <p>Coming Soon...</p>
  </div>
);

function App() {
  return (
    <LanguageProvider>
      <OnboardingProvider>
        <BrowserRouter>
          <Routes>
            {/* Public & Onboarding Routes (No Layout) */}
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />

            <Route path="/onboarding/language" element={<OnboardingGuard><LanguageSelection /></OnboardingGuard>} />
            <Route path="/onboarding/location" element={<OnboardingGuard><LocationSetup /></OnboardingGuard>} />
            <Route path="/onboarding/soil" element={<OnboardingGuard><SoilTypeSelection /></OnboardingGuard>} />
            <Route path="/onboarding/size" element={<OnboardingGuard><FarmSizeInput /></OnboardingGuard>} />
            <Route path="/onboarding/crops" element={<OnboardingGuard><CropSelection /></OnboardingGuard>} />
            <Route path="/onboarding/summary" element={<OnboardingGuard><OnboardingSummary /></OnboardingGuard>} />

            {/* Protected App Routes (With Layout) */}
            <Route path="/" element={<Layout />}>
              <Route path="dashboard" element={<Dashboard />} />
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
            </Route>

            {/* Catch-all */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </OnboardingProvider>
    </LanguageProvider>
  );
}

export default App;
