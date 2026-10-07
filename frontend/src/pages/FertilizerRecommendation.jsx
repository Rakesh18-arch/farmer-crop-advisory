import React, { useState } from 'react';
import { advisoryService } from '../services/advisoryService';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';
import AlertCard from '../components/AlertCard';
import LoadingSpinner from '../components/LoadingSpinner';

const FertilizerRecommendation = () => {
  const { t } = useLanguage();

  const [formData, setFormData] = useState({
    crop: 'Rice',
    target_yield: 2.5,
    n_soil: 80.0,
    p_soil: 40.0,
    k_soil: 40.0,
    farm_size_acres: 2.0
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

  const handleFillSoilFromProfile = async () => {
    try {
      const res = await api.get('/farmer/profile');
      if (res.data.success && res.data.profile) {
        const p = res.data.profile;
        setFormData(prev => ({
          ...prev,
          n_soil: p.n_value || prev.n_soil,
          p_soil: p.p_value || prev.p_soil,
          k_soil: p.k_value || prev.k_soil,
          farm_size_acres: p.farm_size || prev.farm_size_acres
        }));
      }
    } catch {
      setError('Could not auto-fill soil values from profile.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await advisoryService.calculateFertilizer(formData);
      if (data.success) {
        setResult(data);
      } else {
        setError(data.message || 'Error computing fertilizer doses.');
      }
    } catch (err) {
      setError(err?.response?.data?.message || 'Server error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-body">
      <div className="d-flex flex-column flex-sm-row justify-content-between align-items-sm-center gap-3 mb-4">
        <div>
          <h2 className="brand-font mb-1">{t('fertilizer.title')}</h2>
          <p className="text-muted small mb-0">{t('fertilizer.subtitle')}</p>
        </div>
        <button type="button" className="btn btn-outline-success btn-sm" onClick={handleFillSoilFromProfile}>
          <i className="bi bi-droplet-half me-1"></i> Autofill Soil From Profile
        </button>
      </div>

      {error && <AlertCard type="danger" title="Error" message={error} />}

      <div className="row g-4">
        {/* Form Column */}
        <div className="col-12 col-lg-5">
          <div className="agri-card p-4">
            <h5 className="brand-font mb-3 text-warning">
              <i className="bi bi-calculator me-2"></i> Crop & Soil Deficit Inputs
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

              <div className="row g-3 mb-3">
                <div className="col-6">
                  <label className="form-label">Target Yield (Tons/Acre)</label>
                  <input
                    type="number"
                    step="0.1"
                    name="target_yield"
                    className="form-control"
                    value={formData.target_yield}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-6">
                  <label className="form-label">Area (Acres)</label>
                  <input
                    type="number"
                    step="0.5"
                    name="farm_size_acres"
                    className="form-control"
                    value={formData.farm_size_acres}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              <div className="row g-3 mb-4">
                <div className="col-4">
                  <label className="form-label small">Soil N (kg/ha)</label>
                  <input
                    type="number"
                    step="1"
                    name="n_soil"
                    className="form-control"
                    value={formData.n_soil}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-4">
                  <label className="form-label small">Soil P (kg/ha)</label>
                  <input
                    type="number"
                    step="1"
                    name="p_soil"
                    className="form-control"
                    value={formData.p_soil}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-4">
                  <label className="form-label small">Soil K (kg/ha)</label>
                  <input
                    type="number"
                    step="1"
                    name="k_soil"
                    className="form-control"
                    value={formData.k_soil}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              <button type="submit" className="btn btn-agri w-100 py-2" disabled={loading}>
                {loading ? <span className="spinner-border spinner-border-sm me-2"></span> : <i className="bi bi-calculator-fill me-2"></i>}
                {t('fertilizer.btn_calc')}
              </button>
            </form>
          </div>
        </div>

        {/* Results Column */}
        <div className="col-12 col-lg-7">
          {loading && (
            <div className="agri-card p-5 h-100 d-flex align-items-center justify-content-center">
              <LoadingSpinner text="Computing precise stoichiometric nutrient requirements..." />
            </div>
          )}

          {!loading && !result && (
            <div className="agri-card p-5 h-100 d-flex flex-column align-items-center justify-content-center text-center text-muted">
              <div className="fs-1 mb-2">🧪</div>
              <h5 className="brand-font text-dark">No Dosage Computed Yet</h5>
              <p className="small">Fill crop target yield and soil test results to get scientific chemical & organic dosages.</p>
            </div>
          )}

          {!loading && result && (
            <div className="agri-card p-4 h-100">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <span className="badge badge-pill-soft badge-soft-emerald">
                  <i className="bi bi-check2-circle"></i> Fertilizer Recommendation Ready
                </span>
                <span className="text-muted small">Standard ICAR Guidelines</span>
              </div>

              {/* Chemical Fertilizers Cards */}
              <h6 className="fw-bold text-dark mb-2">Chemical Fertilizer Requirements (Total For {formData.farm_size_acres} Acres)</h6>
              <div className="row g-3 mb-4">
                <div className="col-4">
                  <div className="p-3 bg-light rounded border text-center">
                    <small className="text-muted text-uppercase fw-bold">Urea (46% N)</small>
                    <div className="fs-4 fw-bold text-success mt-1">{result.fertilizer?.urea_kg || 120} kg</div>
                    <small className="text-muted">~{Math.ceil((result.fertilizer?.urea_kg || 120) / 45)} Bags (45kg)</small>
                  </div>
                </div>

                <div className="col-4">
                  <div className="p-3 bg-light rounded border text-center">
                    <small className="text-muted text-uppercase fw-bold">DAP (18:46:0)</small>
                    <div className="fs-4 fw-bold text-primary mt-1">{result.fertilizer?.dap_kg || 75} kg</div>
                    <small className="text-muted">~{Math.ceil((result.fertilizer?.dap_kg || 75) / 50)} Bags (50kg)</small>
                  </div>
                </div>

                <div className="col-4">
                  <div className="p-3 bg-light rounded border text-center">
                    <small className="text-muted text-uppercase fw-bold">MOP (60% K)</small>
                    <div className="fs-4 fw-bold text-warning mt-1">{result.fertilizer?.mop_kg || 50} kg</div>
                    <small className="text-muted">~{Math.ceil((result.fertilizer?.mop_kg || 50) / 50)} Bags (50kg)</small>
                  </div>
                </div>
              </div>

              {/* Organic Alternatives */}
              <h6 className="fw-bold text-dark mb-2">Organic & Biological Alternatives</h6>
              <div className="p-3 bg-light rounded border mb-3">
                <div className="d-flex justify-content-between align-items-center mb-2">
                  <span className="fw-bold text-success">🌱 Vermicompost + FYM Mix</span>
                  <span className="badge bg-success">Eco-Friendly</span>
                </div>
                <p className="small text-muted mb-0">
                  Apply <strong>{result.fertilizer?.vermicompost_tons || 1.5} tons/acre</strong> alongside 50 kg Neem Cake per acre to replenish humus and soil microbiota.
                </p>
              </div>

              {/* Application Timings */}
              <div className="p-3 rounded border" style={{ backgroundColor: '#fffbeb' }}>
                <h6 className="fw-bold text-warning mb-1">
                  <i className="bi bi-calendar-check me-1"></i> Split Application Strategy
                </h6>
                <p className="small text-muted mb-0">
                  Apply all DAP and MOP + 33% Urea as basal dose at sowing. Top-dress remaining Urea in 2 equal splits at 30 days (tillering/vegetative) and 60 days (panicle initiation).
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FertilizerRecommendation;
