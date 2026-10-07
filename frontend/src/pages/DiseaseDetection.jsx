import React, { useState } from 'react';
import { diseaseService } from '../services/diseaseService';
import { useLanguage } from '../context/LanguageContext';
import AlertCard from '../components/AlertCard';
import LoadingSpinner from '../components/LoadingSpinner';

const DiseaseDetection = () => {
  const { t } = useLanguage();

  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [cropHint, setCropHint] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError('');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError('');
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError('Please select or upload a plant leaf image first.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await diseaseService.detectDisease(selectedFile, cropHint);
      if (data.success) {
        setResult(data);
      } else {
        setError(data.message || 'Error diagnosing plant leaf.');
      }
    } catch (err) {
      setError(err?.response?.data?.message || 'Server error during disease diagnosis.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-body">
      <div className="mb-4">
        <h2 className="brand-font mb-1">{t('disease.title')}</h2>
        <p className="text-muted small mb-0">{t('disease.subtitle')}</p>
      </div>

      {error && <AlertCard type="danger" title="Error" message={error} />}

      <div className="row g-4">
        {/* Left Column: Image Upload */}
        <div className="col-12 col-lg-5">
          <div className="agri-card p-4">
            <h5 className="brand-font mb-3 text-primary">
              <i className="bi bi-camera me-2"></i> Leaf Image Upload
            </h5>

            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="form-label">Crop Type (Optional Hint)</label>
                <select className="form-select" value={cropHint} onChange={(e) => setCropHint(e.target.value)}>
                  <option value="">Auto-detect crop from photo</option>
                  <option value="Tomato">Tomato</option>
                  <option value="Rice">Rice (Paddy)</option>
                  <option value="Cotton">Cotton</option>
                  <option value="Wheat">Wheat</option>
                  <option value="Maize">Maize</option>
                  <option value="Chilli">Chilli</option>
                  <option value="Potato">Potato</option>
                </select>
              </div>

              {/* Drag and Drop Box */}
              <div
                className="border rounded p-4 text-center mb-3 bg-light"
                style={{ borderStyle: 'dashed !important', borderWidth: '2px', cursor: 'pointer' }}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => document.getElementById('leafFileInput').click()}
              >
                <input
                  type="file"
                  id="leafFileInput"
                  accept="image/*"
                  className="d-none"
                  onChange={handleFileChange}
                />

                {previewUrl ? (
                  <div>
                    <img
                      src={previewUrl}
                      alt="Leaf Preview"
                      className="img-fluid rounded shadow-sm mb-2"
                      style={{ maxHeight: '180px', objectFit: 'cover' }}
                    />
                    <small className="d-block text-success fw-semibold">Click or drop new photo to replace</small>
                  </div>
                ) : (
                  <div>
                    <div className="fs-1 text-primary mb-2">📸</div>
                    <h6 className="fw-bold mb-1">Click to select photo or drag & drop</h6>
                    <small className="text-muted">Supports JPG, PNG, WEBP (Max 10MB)</small>
                  </div>
                )}
              </div>

              <button
                type="submit"
                className="btn btn-agri w-100 py-2"
                disabled={loading || !selectedFile}
              >
                {loading ? <span className="spinner-border spinner-border-sm me-2"></span> : <i className="bi bi-search me-2"></i>}
                {t('disease.btn_scan')}
              </button>
            </form>
          </div>
        </div>

        {/* Right Column: Diagnosis Results */}
        <div className="col-12 col-lg-7">
          {loading && (
            <div className="agri-card p-5 h-100 d-flex align-items-center justify-content-center">
              <LoadingSpinner text="Analyzing leaf chlorosis, lesions, and necrosis patterns with Computer Vision AI..." />
            </div>
          )}

          {!loading && !result && (
            <div className="agri-card p-5 h-100 d-flex flex-column align-items-center justify-content-center text-center text-muted">
              <div className="fs-1 mb-2">🔬</div>
              <h5 className="brand-font text-dark">Awaiting Plant Leaf Upload</h5>
              <p className="small">Upload a photo of an affected leaf to receive automated disease classification and prescription treatments.</p>
            </div>
          )}

          {!loading && result && (
            <div className="agri-card p-4 h-100 shadow-md">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <span className="badge badge-pill-soft badge-soft-emerald">
                  <i className="bi bi-check-circle-fill"></i> Diagnosis Complete
                </span>
                <span className="badge bg-light text-dark border">
                  Target: {result.diagnosis?.detected_crop}
                </span>
              </div>

              {/* Disease Condition Banner */}
              <div className="bg-light p-3 rounded border mb-3">
                <small className="text-muted text-uppercase fw-bold">{t('disease.detected_disease')}</small>
                <h3 className="brand-font text-danger my-1 fw-bold">
                  {result.diagnosis?.detected_disease}
                </h3>
                <div className="d-inline-flex align-items-center gap-2 bg-success text-white px-2 py-1 rounded small">
                  <span>Confidence: {Math.round((result.diagnosis?.confidence || 0.9) * 100)}%</span>
                </div>
              </div>

              {/* Symptoms */}
              <div className="mb-3">
                <h6 className="fw-bold text-dark mb-1">Identified Symptoms</h6>
                <p className="small text-muted mb-0">{result.diagnosis?.symptoms || 'Visible yellow halo lesions and leaf curling observed.'}</p>
              </div>

              {/* Curative Chemical Treatment */}
              <div className="mb-3 p-3 rounded border" style={{ backgroundColor: '#fef2f2' }}>
                <h6 className="fw-bold text-danger mb-1">
                  <i className="bi bi-capsule me-1"></i> {t('disease.treatment')} (Chemical)
                </h6>
                <p className="small text-muted mb-0">{result.diagnosis?.treatment || 'Spray Mancozeb 75% WP @ 2.5 g/L of water.'}</p>
              </div>

              {/* Organic Treatment */}
              <div className="mb-3 p-3 rounded border" style={{ backgroundColor: '#f0fdf4' }}>
                <h6 className="fw-bold text-success mb-1">
                  <i className="bi bi-leaf me-1"></i> {t('disease.organic_treatment')}
                </h6>
                <p className="small text-muted mb-0">{result.diagnosis?.organic_control || 'Spray Neem Oil (10,000 ppm) @ 3 ml/L or apply Trichoderma viride.'}</p>
              </div>

              {/* Prevention Tips */}
              <div>
                <h6 className="fw-bold text-dark mb-1">{t('disease.prevention')}</h6>
                <p className="small text-muted mb-0">{result.diagnosis?.prevention_tips || 'Ensure crop rotation, sanitize tools, and avoid excessive overhead sprinkler watering.'}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DiseaseDetection;
