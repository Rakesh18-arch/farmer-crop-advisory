import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';

const Register = () => {
  const { register } = useAuth();
  const { currentLang, changeLanguage, t } = useLanguage();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    full_name: '',
    phone_number: '',
    email: '',
    password: '',
    state: 'Andhra Pradesh',
    district: 'Guntur',
    village: 'Tenali',
    preferred_language: currentLang
  });

  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await register({ ...formData, preferred_language: currentLang });
      navigate('/');
    } catch (err) {
      setError(err?.response?.data?.message || err.message || 'Registration failed.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-vh-100 d-flex flex-column justify-content-center align-items-center bg-light py-5 px-3">
      <div className="agri-card p-4 p-sm-5 w-100 shadow-md" style={{ maxWidth: '560px' }}>
        <div className="text-center mb-4">
          <div className="sidebar-brand-icon mx-auto mb-2" style={{ width: '52px', height: '52px', fontSize: '1.6rem' }}>
            <span>🌱</span>
          </div>
          <h3 className="brand-font fw-bold mb-1">Farmer Registration</h3>
          <p className="text-muted small mb-0">Join the smart decision platform for personalized crop & fertilizer advisory</p>
        </div>

        {error && (
          <div className="alert alert-danger py-2 px-3 small d-flex align-items-center gap-2 mb-3">
            <i className="bi bi-exclamation-triangle-fill"></i>
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="row g-3">
            <div className="col-12 col-sm-6">
              <label className="form-label">Full Name *</label>
              <input
                type="text"
                name="full_name"
                className="form-control"
                placeholder="e.g. Ramesh Varma"
                value={formData.full_name}
                onChange={handleChange}
                required
              />
            </div>

            <div className="col-12 col-sm-6">
              <label className="form-label">Phone Number *</label>
              <input
                type="tel"
                name="phone_number"
                className="form-control"
                placeholder="10-digit mobile"
                value={formData.phone_number}
                onChange={handleChange}
                required
              />
            </div>

            <div className="col-12 col-sm-6">
              <label className="form-label">Email Address *</label>
              <input
                type="email"
                name="email"
                className="form-control"
                placeholder="farmer@domain.org"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="col-12 col-sm-6">
              <label className="form-label">Password *</label>
              <input
                type="password"
                name="password"
                className="form-control"
                placeholder="Min 6 characters"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>

            <div className="col-12 col-sm-4">
              <label className="form-label">State *</label>
              <select name="state" className="form-select" value={formData.state} onChange={handleChange} required>
                <option value="Andhra Pradesh">Andhra Pradesh</option>
                <option value="Telangana">Telangana</option>
                <option value="Maharashtra">Maharashtra</option>
                <option value="Karnataka">Karnataka</option>
                <option value="Punjab">Punjab</option>
                <option value="Uttar Pradesh">Uttar Pradesh</option>
              </select>
            </div>

            <div className="col-12 col-sm-4">
              <label className="form-label">District *</label>
              <input
                type="text"
                name="district"
                className="form-control"
                placeholder="e.g. Guntur"
                value={formData.district}
                onChange={handleChange}
                required
              />
            </div>

            <div className="col-12 col-sm-4">
              <label className="form-label">Village</label>
              <input
                type="text"
                name="village"
                className="form-control"
                placeholder="e.g. Tenali"
                value={formData.village}
                onChange={handleChange}
              />
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-agri w-100 py-2 mt-4"
            disabled={submitting}
          >
            {submitting ? (
              <span className="spinner-border spinner-border-sm me-2"></span>
            ) : (
              <i className="bi bi-person-plus-fill me-2"></i>
            )}
            Complete Farmer Registration
          </button>
        </form>

        <div className="text-center mt-3">
          <span className="text-muted small">Already registered? </span>
          <Link to="/login" className="text-success fw-bold text-decoration-none small">
            Sign In Here
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Register;
