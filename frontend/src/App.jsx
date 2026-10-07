import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { LanguageProvider } from './context/LanguageContext';

// Components
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Footer from './components/Footer';
import { ProtectedRoute, AdminRoute } from './components/ProtectedRoute';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import FarmerProfile from './pages/FarmerProfile';
import CropRecommendation from './pages/CropRecommendation';
import SoilAnalysis from './pages/SoilAnalysis';
import Weather from './pages/Weather';
import IrrigationAdvisory from './pages/IrrigationAdvisory';
import FertilizerRecommendation from './pages/FertilizerRecommendation';
import DiseaseDetection from './pages/DiseaseDetection';
import PestAdvisory from './pages/PestAdvisory';
import MarketPrices from './pages/MarketPrices';
import GovernmentSchemes from './pages/GovernmentSchemes';
import CropCalendar from './pages/CropCalendar';
import YieldPrediction from './pages/YieldPrediction';
import AIChatbot from './pages/AIChatbot';
import Notifications from './pages/Notifications';
import AdminDashboard from './pages/AdminDashboard';

// Main Layout Shell with Sidebar & Navbar
const AppLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="app-container">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="main-content">
        <Navbar onToggleSidebar={() => setSidebarOpen(prev => !prev)} />
        <main className="flex-grow-1">
          <Outlet />
        </main>
        <Footer />
      </div>
    </div>
  );
};

function App() {
  return (
    <BrowserRouter>
      <LanguageProvider>
        <AuthProvider>
          <Routes>
            {/* Public Auth Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Authenticated Application Shell */}
            <Route
              element={
                <ProtectedRoute>
                  <AppLayout />
                </ProtectedRoute>
              }
            >
              <Route path="/" element={<Dashboard />} />
              <Route path="/profile" element={<FarmerProfile />} />
              <Route path="/crop-recommendation" element={<CropRecommendation />} />
              <Route path="/soil-analysis" element={<SoilAnalysis />} />
              <Route path="/weather" element={<Weather />} />
              <Route path="/irrigation" element={<IrrigationAdvisory />} />
              <Route path="/fertilizer" element={<FertilizerRecommendation />} />
              <Route path="/disease-detection" element={<DiseaseDetection />} />
              <Route path="/pest-advisory" element={<PestAdvisory />} />
              <Route path="/market-prices" element={<MarketPrices />} />
              <Route path="/schemes" element={<GovernmentSchemes />} />
              <Route path="/crop-calendar" element={<CropCalendar />} />
              <Route path="/yield-prediction" element={<YieldPrediction />} />
              <Route path="/chatbot" element={<AIChatbot />} />
              <Route path="/notifications" element={<Notifications />} />

              {/* Admin Protected Route */}
              <Route
                path="/admin"
                element={
                  <AdminRoute>
                    <AdminDashboard />
                  </AdminRoute>
                }
              />
            </Route>

            {/* Catch-all redirect */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </LanguageProvider>
    </BrowserRouter>
  );
}

export default App;
