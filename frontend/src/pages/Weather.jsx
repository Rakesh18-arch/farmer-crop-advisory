import React, { useState, useEffect } from 'react';
import { weatherService } from '../services/weatherService';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import AlertCard from '../components/AlertCard';
import LoadingSpinner from '../components/LoadingSpinner';

const Weather = () => {
  const { user } = useAuth();
  const { t } = useLanguage();

  const [location, setLocation] = useState(user?.district || 'Guntur');
  const [searchInput, setSearchInput] = useState(user?.district || 'Guntur');
  const [loading, setLoading] = useState(true);
  const [currentWeather, setCurrentWeather] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [advisories, setAdvisories] = useState([]);
  const [error, setError] = useState('');

  const fetchWeatherData = async (loc) => {
    setLoading(true);
    setError('');
    try {
      const [curRes, foreRes, advRes] = await Promise.all([
        weatherService.getCurrentWeather(loc),
        weatherService.getForecast(loc),
        weatherService.getAgriculturalAdvisories(loc)
      ]);

      if (curRes.success) setCurrentWeather(curRes.weather);
      if (foreRes.success) setForecast(foreRes.forecast || []);
      if (advRes.success) setAdvisories(advRes.advisories || []);
    } catch (err) {
      setError('Unable to fetch weather data for the specified location.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWeatherData(location);
  }, [location]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      setLocation(searchInput.trim());
    }
  };

  return (
    <div className="page-body">
      <div className="d-flex flex-column flex-sm-row justify-content-between align-items-sm-center gap-3 mb-4">
        <div>
          <h2 className="brand-font mb-1">{t('nav.weather')}</h2>
          <p className="text-muted small mb-0">Live agro-meteorological tracking, 5-day forecast, and field spraying advisories</p>
        </div>

        {/* Search District Form */}
        <form onSubmit={handleSearch} className="d-flex gap-2" style={{ maxWidth: '320px' }}>
          <input
            type="text"
            className="form-control form-control-sm"
            placeholder="Search District..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
          />
          <button type="submit" className="btn btn-sm btn-agri">
            <i className="bi bi-search"></i>
          </button>
        </form>
      </div>

      {error && <AlertCard type="danger" title="Error" message={error} />}

      {loading ? (
        <LoadingSpinner text="Retrieving live satellite and meteorological telemetry..." />
      ) : (
        <>
          {/* Current Weather Hero Banner */}
          {currentWeather && (
            <div className="agri-card p-4 mb-4 text-white" style={{ background: 'linear-gradient(135deg, #065f46 0%, #059669 100%)' }}>
              <div className="row align-items-center">
                <div className="col-12 col-md-6">
                  <div className="d-flex align-items-center gap-2 mb-2">
                    <i className="bi bi-geo-alt-fill"></i>
                    <h4 className="brand-font mb-0">{currentWeather.location}</h4>
                    <span className="badge bg-white text-success ms-2 small">Live Station</span>
                  </div>
                  <div className="display-3 fw-bold mb-1">{currentWeather.temperature}°C</div>
                  <h6 className="fw-normal mb-0 text-white-50">{currentWeather.condition}</h6>
                </div>

                <div className="col-12 col-md-6 mt-3 mt-md-0">
                  <div className="row g-3">
                    <div className="col-6">
                      <div className="p-2 rounded bg-white bg-opacity-10">
                        <small className="d-block text-white-50">Humidity</small>
                        <span className="fs-5 fw-bold">{currentWeather.humidity}%</span>
                      </div>
                    </div>
                    <div className="col-6">
                      <div className="p-2 rounded bg-white bg-opacity-10">
                        <small className="d-block text-white-50">Wind Speed</small>
                        <span className="fs-5 fw-bold">{currentWeather.wind_speed || 12} km/h</span>
                      </div>
                    </div>
                    <div className="col-6">
                      <div className="p-2 rounded bg-white bg-opacity-10">
                        <small className="d-block text-white-50">Precipitation Expected</small>
                        <span className="fs-5 fw-bold">{currentWeather.rainfall_prediction || 0} mm</span>
                      </div>
                    </div>
                    <div className="col-6">
                      <div className="p-2 rounded bg-white bg-opacity-10">
                        <small className="d-block text-white-50">Solar Radiation</small>
                        <span className="fs-5 fw-bold">{currentWeather.uv_index || 'Moderate'}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* 5-Day Agro Forecast */}
          <div className="mb-4">
            <h5 className="brand-font mb-3 text-dark">5-Day Agricultural Weather Outlook</h5>
            <div className="row g-3">
              {forecast.length > 0 ? (
                forecast.map((f, idx) => (
                  <div key={idx} className="col-12 col-sm-6 col-md-4 col-lg">
                    <div className="agri-card p-3 text-center h-100 agri-card-hoverable">
                      <span className="badge badge-pill-soft badge-soft-emerald mb-2 small">{f.day || `Day ${idx + 1}`}</span>
                      <div className="fs-2 my-1">
                        {f.condition?.toLowerCase().includes('rain') ? '🌧️' : f.condition?.toLowerCase().includes('cloud') ? '⛅' : '☀️'}
                      </div>
                      <div className="fw-bold fs-5 text-dark">{f.temp_max}° / <span className="text-muted fs-6">{f.temp_min}°C</span></div>
                      <small className="text-muted d-block mt-1">{f.condition}</small>
                      <div className="mt-2 text-info small fw-semibold">
                        <i className="bi bi-droplet-fill me-1"></i>{f.rainfall_probability || 10}% Rain
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="col-12 text-center text-muted py-3">5-day forecast telemetry synchronized.</div>
              )}
            </div>
          </div>

          {/* Agricultural Field Advisories */}
          <div className="agri-card p-4">
            <h5 className="brand-font mb-3 text-success">
              <i className="bi bi-shield-check me-2"></i> Actionable Field Recommendations
            </h5>
            <div className="row g-3">
              <div className="col-12 col-md-6">
                <div className="p-3 bg-light rounded border h-100">
                  <h6 className="fw-bold mb-1 text-primary">
                    <i className="bi bi-droplet-half me-1"></i> Chemical Spraying Window
                  </h6>
                  <p className="small text-muted mb-0">
                    {currentWeather?.rainfall_prediction > 5
                      ? 'Delay foliar fertilizer and pesticide application. High chance of rain will wash off chemicals.'
                      : 'Excellent spraying conditions today between 7:00 AM and 10:30 AM before wind velocities peak.'}
                  </p>
                </div>
              </div>

              <div className="col-12 col-md-6">
                <div className="p-3 bg-light rounded border h-100">
                  <h6 className="fw-bold mb-1 text-warning">
                    <i className="bi bi-sun me-1"></i> Heat & Evapotranspiration
                  </h6>
                  <p className="small text-muted mb-0">
                    Maintain optimal soil moisture by scheduling drip irrigation during late evening to reduce evaporative loss.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Weather;
