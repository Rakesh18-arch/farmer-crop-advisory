import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';

const Login = () => {
  const { login } = useAuth();
  const { currentLang, changeLanguage, t } = useLanguage();
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError(err?.response?.data?.message || err.message || 'Invalid credentials. Please verify email and password.');
    } finally {
      setSubmitting(false);
    }
  };

  const fillFarmerDemo = () => {
    setEmail('farmer@demo.org');
    setPassword('Farmer@123');
    setError('');
  };

  const fillAdminDemo = () => {
    setEmail('admin@farmeradvisory.org');
    setPassword('Admin@123');
    setError('');
  };

  return (
    <div className="min-vh-100 d-flex flex-column justify-content-center align-items-center bg-light py-5 px-3">
      {/* Language Switcher Bar */}
      <div className="d-flex justify-content-end w-100 mb-3" style={{ maxWidth: '440px' }}>
        <div className="btn-group btn-group-sm">
          <button className={`btn ${currentLang === 'en' ? 'btn-success' : 'btn-outline-secondary'}`} onClick={() => changeLanguage('en')}>English</button>
          <button className={`btn ${currentLang === 'te' ? 'btn-success' : 'btn-outline-secondary'}`} onClick={() => changeLanguage('te')}>తెలుగు</button>
          <button className={`btn ${currentLang === 'hi' ? 'btn-success' : 'btn-outline-secondary'}`} onClick={() => changeLanguage('hi')}>हिन्दी</button>
        </div>
      </div>

      <div className="agri-card p-4 p-sm-5 w-100 shadow-md" style={{ maxWidth: '440px' }}>
        {/* Brand Header */}
        <div className="text-center mb-4">
          <div className="sidebar-brand-icon mx-auto mb-2" style={{ width: '56px', height: '56px', fontSize: '1.8rem' }}>
            <span>🌱</span>
          </div>
          <h3 className="brand-font fw-bold mb-1">{t('app_title')}</h3>
          <p className="text-muted small mb-0">{t('app_subtitle')}</p>
        </div>

        {error && (
          <div className="alert alert-danger py-2 px-3 small d-flex align-items-center gap-2 mb-3">
            <i className="bi bi-exclamation-triangle-fill"></i>
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Email Address</label>
            <div className="input-group">
              <span className="input-group-text bg-white"><i className="bi bi-envelope text-muted"></i></span>
              <input
                type="email"
                className="form-control"
                placeholder="name@farmeradvisory.org"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="mb-3">
            <div className="d-flex justify-content-between align-items-center">
              <label className="form-label mb-0">Password</label>
            </div>
            <div className="input-group mt-1">
              <span className="input-group-text bg-white"><i className="bi bi-lock text-muted"></i></span>
              <input
                type="password"
                className="form-control"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-agri w-100 py-2 mt-2 mb-3"
            disabled={submitting}
          >
            {submitting ? (
              <span className="spinner-border spinner-border-sm me-2"></span>
            ) : (
              <i className="bi bi-box-arrow-in-right me-2"></i>
            )}
            Sign In to Farm Portal
          </button>
        </form>

        {/* Demo Fast-fill Buttons */}
        <div className="border-top pt-3 mt-2 text-center">
          <small className="text-muted d-block mb-2 fw-semibold">Quick Demo 1-Click Credentials:</small>
          <div className="d-flex gap-2">
            <button
              type="button"
              className="btn btn-outline-success btn-sm flex-fill"
              onClick={fillFarmerDemo}
            >
              🧑‍🌾 Farmer Demo
            </button>
            <button
              type="button"
              className="btn btn-outline-secondary btn-sm flex-fill"
              onClick={fillAdminDemo}
            >
              🛡️ Admin Demo
            </button>
          </div>
        </div>

        <div className="text-center mt-4">
          <span className="text-muted small">New farmer? </span>
          <Link to="/register" className="text-success fw-bold text-decoration-none small">
            Register Account
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
