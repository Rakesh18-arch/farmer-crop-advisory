import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { weatherService } from '../services/weatherService';
import { cropService } from '../services/cropService';
import { marketService } from '../services/marketService';
import AlertCard from '../components/AlertCard';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard = () => {
  const { user } = useAuth();
  const { t } = useLanguage();

  const [loading, setLoading] = useState(true);
  const [weatherData, setWeatherData] = useState(null);
  const [recentRecs, setRecentRecs] = useState([]);
  const [marketSnapshot, setMarketSnapshot] = useState([]);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const district = user?.district || 'Guntur';
        const [wRes, hRes, mRes] = await Promise.allSettled([
          weatherService.getCurrentWeather(district),
          cropService.getHistory(),
          marketService.getPrices({ state: user?.state || 'Andhra Pradesh', limit: 4 })
        ]);

        if (wRes.status === 'fulfilled' && wRes.value.success) {
          setWeatherData(wRes.value.weather);
        }
        if (hRes.status === 'fulfilled' && hRes.value.success) {
          setRecentRecs(hRes.value.history.slice(0, 3));
        }
        if (mRes.status === 'fulfilled' && mRes.value.success) {
          setMarketSnapshot(mRes.value.prices.slice(0, 3));
        }
      } catch (err) {
        console.warn('Dashboard data fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, [user]);

  if (loading) {
    return <LoadingSpinner text="Synchronizing farm telemetry and weather data..." />;
  }

  return (
    <div className="page-body">
      {/* Welcome Banner */}
      <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
        <div>
          <h2 className="brand-font mb-1">
            {t('dashboard.welcome')}, {user?.full_name || 'Farmer'}! 👋
          </h2>
          <p className="text-muted small mb-0">
            <i className="bi bi-geo-alt text-danger me-1"></i>
            {user?.village ? `${user.village}, ` : ''}{user?.district || 'Guntur'}, {user?.state || 'Andhra Pradesh'} • Live Agro-Advisory
          </p>
        </div>
        <div className="d-flex gap-2">
          <Link to="/crop-recommendation" className="btn btn-agri">
            <i className="bi bi-flower1 me-1"></i> {t('dashboard.quick_crop_recommend')}
          </Link>
          <Link to="/disease-detection" className="btn btn-agri-outline">
            <i className="bi bi-camera me-1"></i> {t('dashboard.scan_leaf')}
          </Link>
        </div>
      </div>

      {/* Weather Advisory Alert */}
      {weatherData && (
        <AlertCard
          type={weatherData.temperature > 38 ? 'danger' : weatherData.rainfall_prediction > 20 ? 'warning' : 'success'}
          title={`Agro-Weather Alert for ${weatherData.location}: ${weatherData.condition}`}
          message={`${weatherData.temperature}°C with ${weatherData.humidity}% humidity. Rainfall forecast: ${weatherData.rainfall_prediction} mm. Field spray window is favorable during morning hours.`}
          icon="bi-cloud-sun-fill"
        />
      )}

      {/* Top 4 Agri-Metrics Cards */}
      <div className="row g-3 mb-4">
        <div className="col-12 col-sm-6 col-xl-3">
          <div className="agri-stat-card">
            <div className="stat-icon-wrapper stat-icon-emerald">
              <i className="bi bi-tree"></i>
            </div>
            <div>
              <div className="stat-value">{user?.farm_size || '2.5'} <small className="fs-6 fw-normal text-muted">Acres</small></div>
              <div className="stat-label">{t('dashboard.active_farm')} ({user?.soil_type || 'Loamy'})</div>
            </div>
          </div>
        </div>

        <div className="col-12 col-sm-6 col-xl-3">
          <div className="agri-stat-card">
            <div className="stat-icon-wrapper stat-icon-blue">
              <i className="bi bi-thermometer-half"></i>
            </div>
            <div>
              <div className="stat-value">{weatherData?.temperature || 28}°C</div>
              <div className="stat-label">Humidity: {weatherData?.humidity || 65}%</div>
            </div>
          </div>
        </div>

        <div className="col-12 col-sm-6 col-xl-3">
          <div className="agri-stat-card">
            <div className="stat-icon-wrapper stat-icon-amber">
              <i className="bi bi-droplet-half"></i>
            </div>
            <div>
              <div className="stat-value">6.8 <small className="fs-6 fw-normal text-muted">pH</small></div>
              <div className="stat-label">Optimal Soil Reaction</div>
            </div>
          </div>
        </div>

        <div className="col-12 col-sm-6 col-xl-3">
          <div className="agri-stat-card">
            <div className="stat-icon-wrapper stat-icon-purple">
              <i className="bi bi-currency-rupee"></i>
            </div>
            <div>
              <div className="stat-value">₹7,250 <small className="fs-6 fw-normal text-muted">/Q</small></div>
              <div className="stat-label">Cotton (Kurnool Mandi)</div>
            </div>
          </div>
        </div>
      </div>

      {/* Middle Row: Quick Action Hub & Recent Advisories */}
      <div className="row g-4 mb-4">
        <div className="col-12 col-lg-7">
          <div className="agri-card p-4 h-100">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="brand-font mb-0">Agricultural Decision Support Hub</h5>
              <span className="badge badge-pill-soft badge-soft-emerald">AI Ready</span>
            </div>
            <p className="text-muted small mb-4">
              Access real-time machine learning models for crop selection, chemical-deficit calculations, and crop protection.
            </p>

            <div className="row g-3">
              <div className="col-12 col-sm-6">
                <Link to="/crop-recommendation" className="text-decoration-none">
                  <div className="p-3 border rounded agri-card-hoverable bg-light text-dark h-100">
                    <div className="d-flex align-items-center gap-3 mb-2">
                      <div className="bg-success text-white rounded p-2"><i className="bi bi-flower1 fs-5"></i></div>
                      <h6 className="fw-bold mb-0">Crop Recommendation</h6>
                    </div>
                    <small className="text-muted">Multi-feature ML classifier matching NPK, rainfall, and season.</small>
                  </div>
                </Link>
              </div>

              <div className="col-12 col-sm-6">
                <Link to="/disease-detection" className="text-decoration-none">
                  <div className="p-3 border rounded agri-card-hoverable bg-light text-dark h-100">
                    <div className="d-flex align-items-center gap-3 mb-2">
                      <div className="bg-primary text-white rounded p-2"><i className="bi bi-camera fs-5"></i></div>
                      <h6 className="fw-bold mb-0">Plant Leaf Diagnostic</h6>
                    </div>
                    <small className="text-muted">Instant vision detection of fungal and bacterial blight infections.</small>
                  </div>
                </Link>
              </div>

              <div className="col-12 col-sm-6">
                <Link to="/fertilizer" className="text-decoration-none">
                  <div className="p-3 border rounded agri-card-hoverable bg-light text-dark h-100">
                    <div className="d-flex align-items-center gap-3 mb-2">
                      <div className="bg-warning text-dark rounded p-2"><i className="bi bi-calculator fs-5"></i></div>
                      <h6 className="fw-bold mb-0">Fertilizer Calculator</h6>
                    </div>
                    <small className="text-muted">Target yield deficit calculator with organic alternatives.</small>
                  </div>
                </Link>
              </div>

              <div className="col-12 col-sm-6">
                <Link to="/irrigation" className="text-decoration-none">
                  <div className="p-3 border rounded agri-card-hoverable bg-light text-dark h-100">
                    <div className="d-flex align-items-center gap-3 mb-2">
                      <div className="bg-info text-white rounded p-2"><i className="bi bi-moisture fs-5"></i></div>
                      <h6 className="fw-bold mb-0">Smart Irrigation</h6>
                    </div>
                    <small className="text-muted">Growth-stage watering schedule with rain-pause automation.</small>
                  </div>
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: APMC Mandi Rates & Chatbot Callout */}
        <div className="col-12 col-lg-5">
          <div className="agri-card p-4 h-100 d-flex flex-column">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="brand-font mb-0">APMC Mandi Live Trends</h5>
              <Link to="/market-prices" className="text-success small fw-semibold text-decoration-none">View All</Link>
            </div>
            
            <div className="flex-grow-1">
              {marketSnapshot.length > 0 ? (
                <div className="list-group list-group-flush">
                  {marketSnapshot.map((item, idx) => (
                    <div key={idx} className="list-group-item px-0 py-2 d-flex justify-content-between align-items-center">
                      <div>
                        <div className="fw-bold small">{item.commodity} <span className="text-muted fw-normal">({item.market_name})</span></div>
                        <small className="text-muted">{item.variety || 'Standard'}</small>
                      </div>
                      <div className="text-end">
                        <div className="fw-bold text-success">₹{item.modal_price}/Q</div>
                        <small className="text-muted">{item.price_trend === 'UP' ? '▲ Rising' : '▼ Steady'}</small>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-4 text-muted small">
                  <i className="bi bi-graph-up fs-3 d-block mb-2 text-secondary"></i>
                  Connecting to APMC Mandi Price Feeds...
                </div>
              )}
            </div>

            {/* AI Assistant Banner */}
            <div className="p-3 bg-emerald-50 rounded border border-success mt-3" style={{ backgroundColor: '#ecfdf5' }}>
              <div className="d-flex align-items-center gap-3">
                <div className="fs-2">🤖</div>
                <div className="flex-grow-1">
                  <h6 className="fw-bold text-success mb-1">Farmer AI Chatbot</h6>
                  <p className="text-muted small mb-0">Ask questions in English, Telugu, or Hindi.</p>
                </div>
                <Link to="/chatbot" className="btn btn-sm btn-agri">
                  Ask Now
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
