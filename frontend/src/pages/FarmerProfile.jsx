import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import LoadingSpinner from '../components/LoadingSpinner';

const FarmerProfile = () => {
  const { user, refreshUser } = useAuth();
  const { t } = useLanguage();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const [profile, setProfile] = useState({
    farm_size: 2.5,
    farm_location: '',
    soil_type: 'Loamy',
    n_value: 90.0,
    p_value: 42.0,
    k_value: 43.0,
    soil_ph: 6.8,
    soil_moisture: 45.0,
    water_source: 'Borewell',
    irrigation_type: 'Drip Irrigation',
    current_crop: 'Rice',
    previous_crops: 'Cotton, Groundnut'
  });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get('/farmer/profile');
        if (res.data.success && res.data.profile) {
          setProfile(res.data.profile);
        }
      } catch (err) {
        console.warn('Could not load profile:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setProfile(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage({ text: '', type: '' });

    try {
      const res = await api.post('/farmer/profile', profile);
      if (res.data.success) {
        setMessage({ text: 'Farm profile successfully updated!', type: 'success' });
        await refreshUser();
      }
    } catch (err) {
      setMessage({
        text: err?.response?.data?.message || 'Error updating farm profile. Please try again.',
        type: 'danger'
      });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <LoadingSpinner text="Retrieving farm configuration & soil records..." />;
  }

  return (
    <div className="page-body">
      <div className="mb-4">
        <h2 className="brand-font mb-1">{t('nav.profile')}</h2>
        <p className="text-muted small mb-0">Configure your farm attributes, soil nutrients, and water sources for tailored AI models</p>
      </div>

      {message.text && (
        <div className={`alert alert-${message.type} d-flex align-items-center gap-2 mb-4 py-2 px-3 small`}>
          <i className={`bi bi-${message.type === 'success' ? 'check-circle-fill' : 'exclamation-circle-fill'}`}></i>
          <span>{message.text}</span>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="row g-4">
          {/* Farm Dimensions & Agronomics */}
          <div className="col-12 col-lg-6">
            <div className="agri-card p-4 h-100">
              <h5 className="brand-font mb-3 d-flex align-items-center gap-2 text-success">
                <i className="bi bi-geo-alt"></i> Land & Cultivation Overview
              </h5>

              <div className="row g-3">
                <div className="col-12 col-sm-6">
                  <label className="form-label">Total Land Size (Acres) *</label>
                  <input
                    type="number"
                    step="0.1"
                    name="farm_size"
                    className="form-control"
                    value={profile.farm_size}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-12 col-sm-6">
                  <label className="form-label">Primary Soil Classification *</label>
                  <select name="soil_type" className="form-select" value={profile.soil_type} onChange={handleChange}>
                    <option value="Loamy">Loamy (High fertility)</option>
                    <option value="Black">Black Soil (Regur)</option>
                    <option value="Red">Red Soil (Chalka)</option>
                    <option value="Alluvial">Alluvial (River basin)</option>
                    <option value="Clay">Clay Soil</option>
                    <option value="Sandy">Sandy Loam</option>
                  </select>
                </div>

                <div className="col-12 col-sm-6">
                  <label className="form-label">Currently Growing Crop</label>
                  <input
                    type="text"
                    name="current_crop"
                    className="form-control"
                    placeholder="e.g. Rice, Cotton, Tomato"
                    value={profile.current_crop || ''}
                    onChange={handleChange}
                  />
                </div>

                <div className="col-12 col-sm-6">
                  <label className="form-label">Previous Crop Rotation</label>
                  <input
                    type="text"
                    name="previous_crops"
                    className="form-control"
                    placeholder="e.g. Groundnut, Maize"
                    value={profile.previous_crops || ''}
                    onChange={handleChange}
                  />
                </div>

                <div className="col-12 col-sm-6">
                  <label className="form-label">Water Source</label>
                  <select name="water_source" className="form-select" value={profile.water_source} onChange={handleChange}>
                    <option value="Borewell">Borewell</option>
                    <option value="Canal">Canal Irrigation</option>
                    <option value="Rainfed">Rainfed (Dryland)</option>
                    <option value="Well">Open Well</option>
                    <option value="River">River Lift</option>
                  </select>
                </div>

                <div className="col-12 col-sm-6">
                  <label className="form-label">Irrigation System</label>
                  <select name="irrigation_type" className="form-select" value={profile.irrigation_type} onChange={handleChange}>
                    <option value="Drip Irrigation">Drip Irrigation (High efficiency)</option>
                    <option value="Sprinkler">Sprinkler System</option>
                    <option value="Flood">Flood / Furrow Irrigation</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Soil Telemetry & Nutrients */}
          <div className="col-12 col-lg-6">
            <div className="agri-card p-4 h-100">
              <h5 className="brand-font mb-3 d-flex align-items-center gap-2 text-success">
                <i className="bi bi-droplet-half"></i> Baseline Soil Chemistry (Health Card)
              </h5>
              <p className="text-muted small mb-3">
                Values obtained from your local Krishi Vigyan Kendra (KVK) or Soil Testing Laboratory.
              </p>

              <div className="row g-3">
                <div className="col-12 col-sm-4">
                  <label className="form-label">Nitrogen (N) kg/ha</label>
                  <input
                    type="number"
                    step="1"
                    name="n_value"
                    className="form-control"
                    value={profile.n_value}
                    onChange={handleChange}
                    required
                  />
                  <small className="text-muted d-block mt-1">Optimal: 60 - 120</small>
                </div>

                <div className="col-12 col-sm-4">
                  <label className="form-label">Phosphorus (P) kg/ha</label>
                  <input
                    type="number"
                    step="1"
                    name="p_value"
                    className="form-control"
                    value={profile.p_value}
                    onChange={handleChange}
                    required
                  />
                  <small className="text-muted d-block mt-1">Optimal: 35 - 60</small>
                </div>

                <div className="col-12 col-sm-4">
                  <label className="form-label">Potassium (K) kg/ha</label>
                  <input
                    type="number"
                    step="1"
                    name="k_value"
                    className="form-control"
                    value={profile.k_value}
                    onChange={handleChange}
                    required
                  />
                  <small className="text-muted d-block mt-1">Optimal: 35 - 50</small>
                </div>

                <div className="col-12 col-sm-6">
                  <label className="form-label">Soil pH (0 - 14)</label>
                  <input
                    type="number"
                    step="0.1"
                    name="soil_ph"
                    className="form-control"
                    value={profile.soil_ph}
                    onChange={handleChange}
                    required
                  />
                  <small className="text-muted d-block mt-1">Optimal: 6.0 - 7.5</small>
                </div>

                <div className="col-12 col-sm-6">
                  <label className="form-label">Soil Moisture Content (%)</label>
                  <input
                    type="number"
                    step="1"
                    name="soil_moisture"
                    className="form-control"
                    value={profile.soil_moisture}
                    onChange={handleChange}
                    required
                  />
                  <small className="text-muted d-block mt-1">Optimal: 40 - 60%</small>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="d-flex justify-content-end mt-4">
          <button type="submit" className="btn btn-agri px-4 py-2" disabled={saving}>
            {saving ? (
              <span className="spinner-border spinner-border-sm me-2"></span>
            ) : (
              <i className="bi bi-cloud-check-fill me-2"></i>
            )}
            Save & Update Farm Telemetry
          </button>
        </div>
      </form>
    </div>
  );
};

export default FarmerProfile;
