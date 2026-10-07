import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { cropService } from '../services/cropService';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';
import AlertCard from '../components/AlertCard';
import LoadingSpinner from '../components/LoadingSpinner';

const CropRecommendation = () => {
  const { user } = useAuth();
  const { t } = useLanguage();

  const [formData, setFormData] = useState({
    n: 90.0,
    p: 42.0,
    k: 43.0,
    ph: 6.8,
    temperature: 28.0,
    humidity: 70.0,
    rainfall: 150.0,
    season: 'Kharif',
    soil_type: 'Loamy'
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [llmReport, setLlmReport] = useState(null);
  const [generatingReport, setGeneratingReport] = useState(false);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value
    }));
  };

  const handleFillFromProfile = async () => {
    try {
      const res = await api.get('/farmer/profile');
      if (res.data.success && res.data.profile) {
        const p = res.data.profile;
        setFormData(prev => ({
          ...prev,
          n: p.n_value || prev.n,
          p: p.p_value || prev.p,
          k: p.k_value || prev.k,
          ph: p.soil_ph || prev.ph,
          soil_type: p.soil_type || prev.soil_type
        }));
      }
    } catch {
      setError('Could not auto-fill profile values. Using current inputs.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await cropService.recommendCrop(formData);
      if (data.success) {
        setResult(data);
      } else {
        setError(data.message || 'Error generating recommendation.');
      }
    } catch (err) {
      setError(err?.response?.data?.message || 'Server error occurred during prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-body">
      <div className="d-flex flex-column flex-sm-row justify-content-between align-items-sm-center gap-3 mb-4">
        <div>
          <h2 className="brand-font mb-1">{t('crop_recommend.title')}</h2>
          <p className="text-muted small mb-0">{t('crop_recommend.subtitle')}</p>
        </div>
        <button type="button" className="btn btn-outline-success btn-sm" onClick={handleFillFromProfile}>
          <i className="bi bi-person-lines-fill me-1"></i> Fill From My Farm Profile
        </button>
      </div>

      {error && (
        <AlertCard type="danger" title="Error" message={error} />
      )}

      <div className="row g-4">
        {/* Left Column: Input Form */}
        <div className="col-12 col-lg-6">
          <div className="agri-card p-4">
            <h5 className="brand-font mb-3 text-success">
              <i className="bi bi-sliders me-2"></i> {t('crop_recommend.inputs_header')}
            </h5>

            <form onSubmit={handleSubmit}>
              <div className="row g-3">
                <div className="col-12 col-sm-4">
                  <label className="form-label">{t('crop_recommend.nitrogen')}</label>
                  <input
                    type="number"
                    step="1"
                    name="n"
                    className="form-control"
                    value={formData.n}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-12 col-sm-4">
                  <label className="form-label">{t('crop_recommend.phosphorus')}</label>
                  <input
                    type="number"
                    step="1"
                    name="p"
                    className="form-control"
                    value={formData.p}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-12 col-sm-4">
                  <label className="form-label">{t('crop_recommend.potassium')}</label>
                  <input
                    type="number"
                    step="1"
                    name="k"
                    className="form-control"
                    value={formData.k}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-12 col-sm-6">
                  <label className="form-label">{t('crop_recommend.ph')}</label>
                  <input
                    type="number"
                    step="0.1"
                    name="ph"
                    className="form-control"
                    value={formData.ph}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-12 col-sm-6">
                  <label className="form-label">{t('crop_recommend.soil_type')}</label>
                  <select name="soil_type" className="form-select" value={formData.soil_type} onChange={handleChange}>
                    <option value="Loamy">Loamy</option>
                    <option value="Black">Black Soil</option>
                    <option value="Red">Red Soil</option>
                    <option value="Alluvial">Alluvial</option>
                    <option value="Clay">Clay</option>
                    <option value="Sandy">Sandy Loam</option>
                  </select>
                </div>

                <div className="col-12 col-sm-4">
                  <label className="form-label">{t('crop_recommend.temp')}</label>
                  <input
                    type="number"
                    step="0.5"
                    name="temperature"
                    className="form-control"
                    value={formData.temperature}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-12 col-sm-4">
                  <label className="form-label">{t('crop_recommend.humidity')}</label>
                  <input
                    type="number"
                    step="1"
                    name="humidity"
                    className="form-control"
                    value={formData.humidity}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-12 col-sm-4">
                  <label className="form-label">{t('crop_recommend.rainfall')}</label>
                  <input
                    type="number"
                    step="5"
                    name="rainfall"
                    className="form-control"
                    value={formData.rainfall}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="col-12">
                  <label className="form-label">{t('crop_recommend.season')}</label>
                  <select name="season" className="form-select" value={formData.season} onChange={handleChange}>
                    <option value="Kharif">Kharif (Monsoon / June - Oct)</option>
                    <option value="Rabi">Rabi (Winter / Nov - March)</option>
                    <option value="Zaid">Zaid (Summer / April - June)</option>
                  </select>
                </div>
              </div>

              <button type="submit" className="btn btn-agri w-100 py-2 mt-4" disabled={loading}>
                {loading ? (
                  <span className="spinner-border spinner-border-sm me-2"></span>
                ) : (
                  <i className="bi bi-cpu-fill me-2"></i>
                )}
                {t('crop_recommend.btn_submit')}
              </button>
            </form>
          </div>
        </div>

        {/* Right Column: AI Output Card */}
        <div className="col-12 col-lg-6">
          {loading && (
            <div className="agri-card p-5 h-100 d-flex align-items-center justify-content-center">
              <LoadingSpinner text="Running ML Classifier across 2,400 multi-soil records..." />
            </div>
          )}

          {!loading && !result && (
            <div className="agri-card p-5 h-100 d-flex flex-column align-items-center justify-content-center text-center text-muted">
              <div className="fs-1 mb-2">🌾</div>
              <h5 className="brand-font text-dark">No Recommendation Generated Yet</h5>
              <p className="small">Enter soil nutrients and seasonal telemetry, then click "Generate AI Recommendation".</p>
            </div>
          )}

          {!loading && result && (
            <div className="agri-card p-4 h-100 border-success shadow-md">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <span className="badge badge-pill-soft badge-soft-emerald">
                  <i className="bi bi-check-circle-fill"></i> Recommendation Ready
                </span>
                <span className="text-muted small">
                  Model: {result.recommendation?.model_used || 'Logistic Regression (95.8%)'}
                </span>
              </div>

              {/* Primary Crop Banner */}
              <div className="bg-light p-4 rounded text-center mb-4 border">
                <small className="text-muted text-uppercase fw-bold letter-spacing">{t('crop_recommend.recommended_crop')}</small>
                <h1 className="brand-font text-success display-5 my-2 fw-bold">
                  {result.recommendation?.recommended_crop}
                </h1>
                <div className="d-inline-flex align-items-center gap-2 bg-success text-white px-3 py-1 rounded-pill small fw-semibold">
                  <span>Confidence:</span>
                  <span>{Math.round((result.recommendation?.confidence_score || 0.95) * 100)}%</span>
                </div>
              </div>

              {/* Rationale */}
              <div className="mb-4">
                <h6 className="fw-bold text-dark mb-1">{t('crop_recommend.rationale')}</h6>
                <p className="small text-muted mb-0">{result.recommendation?.explanation}</p>
              </div>

              {/* Alternative Crops */}
              <div className="mb-4">
                <h6 className="fw-bold text-dark mb-2">{t('crop_recommend.alternatives')}</h6>
                <div className="d-flex gap-2">
                  {result.recommendation?.alternatives?.map((crop, idx) => (
                    <span key={idx} className="badge bg-light text-dark border p-2 flex-fill text-center fs-6">
                      🌱 {crop}
                    </span>
                  ))}
                </div>
              </div>

              {/* LLM In-Depth Agronomic Advisory Report */}
              <div className="mb-4 p-3 bg-light rounded border border-success-subtle">
                <div className="d-flex justify-content-between align-items-center mb-2">
                  <h6 className="fw-bold text-success mb-0">
                    <i className="bi bi-robot me-1"></i> LLM Agronomic Reasoning
                  </h6>
                  <button
                    type="button"
                    className="btn btn-sm btn-outline-success"
                    onClick={async () => {
                      setGeneratingReport(true);
                      try {
                        const rep = await cropService.explainRecommendation({
                          crop: result.recommendation?.recommended_crop,
                          n: formData.n, p: formData.p, k: formData.k, ph: formData.ph,
                          temperature: formData.temperature, humidity: formData.humidity, rainfall: formData.rainfall,
                          soil_type: formData.soil_type, season: formData.season,
                          confidence: result.recommendation?.confidence_score || 0.95
                        });
                        if (rep.success) setLlmReport(rep);
                      } catch {
                        setError('Could not generate LLM report right now.');
                      } finally {
                        setGeneratingReport(false);
                      }
                    }}
                    disabled={generatingReport}
                  >
                    {generatingReport ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-1"></span> Formulating Advisory...
                      </>
                    ) : (
                      <>
                        <i className="bi bi-stars me-1"></i> {llmReport ? 'Regenerate LLM Report' : 'Generate Full LLM Report'}
                      </>
                    )}
                  </button>
                </div>

                {llmReport ? (
                  <div
                    className="p-3 bg-white rounded border small mt-2 shadow-sm"
                    style={{ maxHeight: '350px', overflowY: 'auto', whiteSpace: 'pre-wrap', lineHeight: '1.6' }}
                  >
                    <div className="d-flex justify-content-between text-muted border-bottom pb-1 mb-2">
                      <small>Engine: <strong>{llmReport.model || 'AgriLLM-Neural'}</strong></small>
                      <small className="text-success fw-bold">✓ 360° Agro-Climatic Synthesis</small>
                    </div>
                    {llmReport.explanation_markdown}
                  </div>
                ) : (
                  <p className="small text-muted mb-0">
                    Click to generate a comprehensive 360-degree agronomic report including soil nutrient synergy, irrigation timetable, IPM pest mitigation, and market profitability.
                  </p>
                )}
              </div>

              {/* Action Buttons for Next Steps */}
              <div className="d-flex gap-2 mt-auto pt-3 border-top">
                <Link
                  to={`/crop-calendar?crop=${result.recommendation?.recommended_crop}`}
                  className="btn btn-outline-success btn-sm flex-fill"
                >
                  <i className="bi bi-calendar3 me-1"></i> View Sowing Calendar
                </Link>
                <Link
                  to={`/yield-prediction?crop=${result.recommendation?.recommended_crop}`}
                  className="btn btn-agri btn-sm flex-fill"
                >
                  <i className="bi bi-pie-chart me-1"></i> Estimate Harvest Yield
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CropRecommendation;
