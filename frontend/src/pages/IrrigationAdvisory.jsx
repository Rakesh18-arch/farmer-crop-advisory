import React, { useState } from 'react';
import { advisoryService } from '../services/advisoryService';
import { useLanguage } from '../context/LanguageContext';
import AlertCard from '../components/AlertCard';
import LoadingSpinner from '../components/LoadingSpinner';

const IrrigationAdvisory = () => {
  const { t } = useLanguage();

  const [formData, setFormData] = useState({
    crop: 'Rice',
    growth_stage: 'Vegetative',
    soil_type: 'Loamy',
    area_acres: 2.5,
    irrigation_method: 'Drip'
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await advisoryService.getIrrigationSchedule(formData);
      if (data.success) {
        setResult(data);
      } else {
        setError(data.message || 'Unable to compute irrigation schedule.');
      }
    } catch (err) {
      setError(err?.response?.data?.message || 'Server error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-body">
      <div className="mb-4">
        <h2 className="brand-font mb-1">{t('nav.irrigation')}</h2>
        <p className="text-muted small mb-0">Compute smart watering schedules based on crop evapotranspiration and rainfall forecasts</p>
      </div>

      {error && <AlertCard type="danger" title="Error" message={error} />}

      <div className="row g-4">
        {/* Form Column */}
        <div className="col-12 col-lg-5">
          <div className="agri-card p-4">
            <h5 className="brand-font mb-3 text-info">
              <i className="bi bi-droplet-half me-2"></i> Field Telemetry
            </h5>

            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="form-label">Crop Name *</label>
                <select name="crop" className="form-select" value={formData.crop} onChange={handleChange}>
                  <option value="Rice">Rice (Paddy)</option>
                  <option value="Cotton">Cotton</option>
                  <option value="Tomato">Tomato</option>
                  <option value="Wheat">Wheat</option>
                  <option value="Maize">Maize</option>
                  <option value="Sugarcane">Sugarcane</option>
                  <option value="Groundnut">Groundnut</option>
                  <option value="Chilli">Chilli</option>
                </select>
              </div>

              <div className="mb-3">
                <label className="form-label">Phenological Growth Stage *</label>
                <select name="growth_stage" className="form-select" value={formData.growth_stage} onChange={handleChange}>
                  <option value="Germination">Initial / Germination</option>
                  <option value="Vegetative">Vegetative Growth</option>
                  <option value="Flowering">Flowering / Tasseling (Critical)</option>
                  <option value="Grain Filling">Grain Filling / Fruit Development</option>
                  <option value="Maturity">Maturity / Ripening</option>
                </select>
              </div>

              <div className="mb-3">
                <label className="form-label">Soil Classification</label>
                <select name="soil_type" className="form-select" value={formData.soil_type} onChange={handleChange}>
                  <option value="Loamy">Loamy (Moderate retention)</option>
                  <option value="Clay">Clay (High retention)</option>
                  <option value="Sandy">Sandy (Low retention / High drainage)</option>
                  <option value="Black">Black Soil (High swell / Shrink)</option>
                </select>
              </div>

              <div className="mb-3">
                <label className="form-label">Cultivated Area (Acres)</label>
                <input
                  type="number"
                  step="0.5"
                  name="area_acres"
                  className="form-control"
                  value={formData.area_acres}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="mb-4">
                <label className="form-label">Irrigation System</label>
                <select name="irrigation_method" className="form-select" value={formData.irrigation_method} onChange={handleChange}>
                  <option value="Drip">Drip Irrigation (90% Efficiency)</option>
                  <option value="Sprinkler">Sprinkler (75% Efficiency)</option>
                  <option value="Flood">Flood / Furrow (50% Efficiency)</option>
                </select>
              </div>

              <button type="submit" className="btn btn-agri w-100 py-2" disabled={loading}>
                {loading ? <span className="spinner-border spinner-border-sm me-2"></span> : <i className="bi bi-moisture me-2"></i>}
                Calculate Watering Schedule
              </button>
            </form>
          </div>
        </div>

        {/* Results Column */}
        <div className="col-12 col-lg-7">
          {loading && (
            <div className="agri-card p-5 h-100 d-flex align-items-center justify-content-center">
              <LoadingSpinner text="Computing crop water deficit with FAO-56 Penman-Monteith algorithms..." />
            </div>
          )}

          {!loading && !result && (
            <div className="agri-card p-5 h-100 d-flex flex-column align-items-center justify-content-center text-center text-muted">
              <div className="fs-1 mb-2">💧</div>
              <h5 className="brand-font text-dark">No Schedule Generated Yet</h5>
              <p className="small">Select your crop and growth stage to compute precise liters/acre and run times.</p>
            </div>
          )}

          {!loading && result && (
            <div className="agri-card p-4 h-100">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <span className="badge badge-pill-soft badge-soft-blue">
                  <i className="bi bi-water"></i> Smart Irrigation Schedule
                </span>
                <span className="text-muted small">Algorithm: FAO-56 Evapotranspiration</span>
              </div>

              {/* Water Metric Cards */}
              <div className="row g-3 mb-4">
                <div className="col-12 col-sm-6">
                  <div className="p-3 bg-light rounded border text-center">
                    <small className="text-muted text-uppercase fw-bold">Next Irrigation Date</small>
                    <div className="fs-4 fw-bold text-primary mt-1">
                      {result.advisory?.recommended_date || 'Tomorrow Morning'}
                    </div>
                  </div>
                </div>

                <div className="col-12 col-sm-6">
                  <div className="p-3 bg-light rounded border text-center">
                    <small className="text-muted text-uppercase fw-bold">Water Volume Required</small>
                    <div className="fs-4 fw-bold text-success mt-1">
                      {result.advisory?.water_liters_per_acre || '18,500'} <small className="fs-6">Liters/Acre</small>
                    </div>
                  </div>
                </div>
              </div>

              {/* Pump Operation Guidance */}
              <div className="p-3 rounded border mb-3" style={{ backgroundColor: '#f0fdf4' }}>
                <h6 className="fw-bold text-success mb-1">
                  <i className="bi bi-clock-history me-1"></i> Pump / Valve Operation Time
                </h6>
                <p className="small mb-0 text-muted">
                  Run standard 5 HP pump for <strong>{result.advisory?.run_time_hours || '2.5'} hours</strong> per acre to reach effective field capacity.
                </p>
              </div>

              {/* Critical Growth Stage Note */}
              <div className="p-3 rounded border mb-3 bg-light">
                <h6 className="fw-bold text-dark mb-1">Critical Stage Sensitivity</h6>
                <p className="small text-muted mb-0">
                  {formData.growth_stage === 'Flowering'
                    ? 'CRITICAL WARNING: Flowering is the moisture-stress sensitive stage. Moisture deficits now will cause flower drop and significant yield reduction.'
                    : 'Maintain regular intervals. Avoid water accumulation at base to prevent root rot.'}
                </p>
              </div>

              {/* Rain Automation Note */}
              <div className="p-3 rounded border bg-light">
                <h6 className="fw-bold text-dark mb-1">
                  <i className="bi bi-cloud-rain text-primary me-1"></i> Weather Rain-Pause Automation
                </h6>
                <p className="small text-muted mb-0">
                  If rainfall exceeds 15 mm within 24 hours, postpone this irrigation event by 48 hours to conserve groundwater.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default IrrigationAdvisory;
