import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import LoadingSpinner from '../components/LoadingSpinner';

const SoilAnalysis = () => {
  const { user } = useAuth();
  const { t } = useLanguage();

  const [loading, setLoading] = useState(true);
  const [soil, setSoil] = useState({
    n: 90.0,
    p: 42.0,
    k: 43.0,
    ph: 6.8,
    moisture: 45.0,
    soil_type: 'Loamy'
  });

  useEffect(() => {
    const fetchSoil = async () => {
      try {
        const res = await api.get('/farmer/profile');
        if (res.data.success && res.data.profile) {
          const p = res.data.profile;
          setSoil({
            n: p.n_value || 90.0,
            p: p.p_value || 42.0,
            k: p.k_value || 43.0,
            ph: p.soil_ph || 6.8,
            moisture: p.soil_moisture || 45.0,
            soil_type: p.soil_type || 'Loamy'
          });
        }
      } catch (err) {
        console.warn('Error fetching soil data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSoil();
  }, []);

  const getNutrientStatus = (val, minOpt, maxOpt) => {
    if (val < minOpt) return { status: 'Deficient (Low)', color: 'danger', percent: Math.min(100, (val / minOpt) * 50) };
    if (val > maxOpt) return { status: 'High / Surplus', color: 'warning', percent: 95 };
    return { status: 'Optimal (Healthy)', color: 'success', percent: 75 };
  };

  const nStatus = getNutrientStatus(soil.n, 60, 120);
  const pStatus = getNutrientStatus(soil.p, 35, 60);
  const kStatus = getNutrientStatus(soil.k, 35, 50);

  const getPhStatus = (ph) => {
    if (ph < 6.0) return { status: 'Acidic (Apply Agricultural Lime)', color: 'warning' };
    if (ph > 7.8) return { status: 'Alkaline (Apply Gypsum / Organic Mulch)', color: 'warning' };
    return { status: 'Optimal Neutral (6.0 - 7.5)', color: 'success' };
  };
  const phStatus = getPhStatus(soil.ph);

  if (loading) {
    return <LoadingSpinner text="Analyzing Soil Health parameters..." />;
  }

  return (
    <div className="page-body">
      <div className="mb-4">
        <h2 className="brand-font mb-1">{t('nav.soil_analysis')}</h2>
        <p className="text-muted small mb-0">ICAR Soil Health Card telemetry with nutrient deficit remediation guidelines</p>
      </div>

      <div className="row g-4">
        {/* Soil Health Card */}
        <div className="col-12 col-lg-7">
          <div className="agri-card p-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="brand-font mb-0 text-success">
                <i className="bi bi-card-checklist me-2"></i> Digital Soil Health Card
              </h5>
              <span className="badge badge-pill-soft badge-soft-emerald">Classification: {soil.soil_type}</span>
            </div>

            <div className="mb-4">
              <div className="d-flex justify-content-between align-items-center mb-1">
                <span className="fw-semibold small">Available Nitrogen (N)</span>
                <span className={`badge bg-${nStatus.color} small`}>{nStatus.status} • {soil.n} kg/ha</span>
              </div>
              <div className="progress" style={{ height: '10px' }}>
                <div className={`progress-bar bg-${nStatus.color}`} style={{ width: `${nStatus.percent}%` }}></div>
              </div>
              <small className="text-muted">Benchmark optimal range: 60 - 120 kg/ha</small>
            </div>

            <div className="mb-4">
              <div className="d-flex justify-content-between align-items-center mb-1">
                <span className="fw-semibold small">Available Phosphorus (P)</span>
                <span className={`badge bg-${pStatus.color} small`}>{pStatus.status} • {soil.p} kg/ha</span>
              </div>
              <div className="progress" style={{ height: '10px' }}>
                <div className={`progress-bar bg-${pStatus.color}`} style={{ width: `${pStatus.percent}%` }}></div>
              </div>
              <small className="text-muted">Benchmark optimal range: 35 - 60 kg/ha</small>
            </div>

            <div className="mb-4">
              <div className="d-flex justify-content-between align-items-center mb-1">
                <span className="fw-semibold small">Available Potassium (K)</span>
                <span className={`badge bg-${kStatus.color} small`}>{kStatus.status} • {soil.k} kg/ha</span>
              </div>
              <div className="progress" style={{ height: '10px' }}>
                <div className={`progress-bar bg-${kStatus.color}`} style={{ width: `${kStatus.percent}%` }}></div>
              </div>
              <small className="text-muted">Benchmark optimal range: 35 - 50 kg/ha</small>
            </div>

            <div className="mb-4">
              <div className="d-flex justify-content-between align-items-center mb-1">
                <span className="fw-semibold small">Soil Reaction (pH)</span>
                <span className={`badge bg-${phStatus.color} small`}>{phStatus.status} • {soil.ph} pH</span>
              </div>
              <div className="progress" style={{ height: '10px' }}>
                <div className={`progress-bar bg-${phStatus.color}`} style={{ width: `${(soil.ph / 14) * 100}%` }}></div>
              </div>
              <small className="text-muted">Ideal neutral agricultural range: 6.0 - 7.5</small>
            </div>

            <div>
              <div className="d-flex justify-content-between align-items-center mb-1">
                <span className="fw-semibold small">Volumetric Moisture Content</span>
                <span className="badge bg-info small">{soil.moisture}% Moisture</span>
              </div>
              <div className="progress" style={{ height: '10px' }}>
                <div className="progress-bar bg-info" style={{ width: `${soil.moisture}%` }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Agronomic Recommendations Panel */}
        <div className="col-12 col-lg-5">
          <div className="agri-card p-4 h-100">
            <h5 className="brand-font mb-3 text-dark">
              <i className="bi bi-shield-plus text-success me-2"></i> Soil Remediation Guidelines
            </h5>

            <div className="mb-3 p-3 bg-light rounded border">
              <h6 className="fw-bold mb-1 text-success">1. Organic Carbon Augmentation</h6>
              <p className="small text-muted mb-0">
                Incorporate 2 to 3 tons of well-rotted Farm Yard Manure (FYM) or Vermicompost per acre during land preparation to boost cation-exchange capacity.
              </p>
            </div>

            <div className="mb-3 p-3 bg-light rounded border">
              <h6 className="fw-bold mb-1 text-success">2. Bio-fertilizer Inoculation</h6>
              <p className="small text-muted mb-0">
                Treat seeds with <em>Azospirillum</em> (for cereals) or <em>Rhizobium</em> (for pulses) alongside Phosphate Solubilizing Bacteria (PSB) at 200g per 10kg seed.
              </p>
            </div>

            <div className="p-3 bg-light rounded border">
              <h6 className="fw-bold mb-1 text-success">3. Micronutrient Balance</h6>
              <p className="small text-muted mb-0">
                If cultivating rice, maize, or cotton, apply Zinc Sulfate (ZnSO₄) @ 10 kg/acre to prevent Khaira and leaf bronzing diseases.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SoilAnalysis;
