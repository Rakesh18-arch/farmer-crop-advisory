import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { notificationService } from '../services/notificationService';

const Navbar = ({ onToggleSidebar }) => {
  const { user, isAuthenticated, isAdmin, logout } = useAuth();
  const { currentLang, changeLanguage, t } = useLanguage();
  const navigate = useNavigate();

  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    if (isAuthenticated) {
      notificationService.getNotifications()
        .then(res => {
          if (res.success) setUnreadCount(res.unread_count || 0);
        })
        .catch(() => {});
    }
  }, [isAuthenticated]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="top-navbar">
      <div className="d-flex align-items-center gap-3">
        <button
          className="btn btn-sm btn-light d-lg-none"
          onClick={onToggleSidebar}
          aria-label="Toggle navigation"
        >
          <i className="bi bi-list fs-5"></i>
        </button>
        <span className="badge badge-pill-soft badge-soft-emerald d-none d-md-inline-flex">
          <i className="bi bi-shield-check"></i> ICAR & APMC Verified
        </span>
      </div>

      <div className="d-flex align-items-center gap-3">
        {/* Language Selector */}
        <div className="dropdown">
          <button
            className="btn btn-sm btn-outline-secondary dropdown-toggle d-flex align-items-center gap-2"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            <i className="bi bi-translate text-success"></i>
            <span className="text-uppercase fw-semibold">{currentLang}</span>
          </button>
          <ul className="dropdown-menu dropdown-menu-end shadow-sm">
            <li>
              <button
                className={`dropdown-item ${currentLang === 'en' ? 'active bg-success' : ''}`}
                onClick={() => changeLanguage('en')}
              >
                English (Default)
              </button>
            </li>
            <li>
              <button
                className={`dropdown-item ${currentLang === 'te' ? 'active bg-success' : ''}`}
                onClick={() => changeLanguage('te')}
              >
                తెలుగు (Telugu)
              </button>
            </li>
            <li>
              <button
                className={`dropdown-item ${currentLang === 'hi' ? 'active bg-success' : ''}`}
                onClick={() => changeLanguage('hi')}
              >
                हिन्दी (Hindi)
              </button>
            </li>
          </ul>
        </div>

        {/* Notifications Icon */}
        {isAuthenticated && (
          <Link to="/notifications" className="btn btn-sm btn-light position-relative p-2" title="Notifications">
            <i className="bi bi-bell fs-6"></i>
            {unreadCount > 0 && (
              <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style={{ fontSize: '0.65rem' }}>
                {unreadCount}
              </span>
            )}
          </Link>
        )}

        {/* User Account / Auth buttons */}
        {isAuthenticated ? (
          <div className="dropdown">
            <button
              className="btn btn-sm btn-light dropdown-toggle d-flex align-items-center gap-2 border"
              type="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <div
                className="bg-success text-white rounded-circle d-flex align-items-center justify-content-center fw-bold"
                style={{ width: '28px', height: '28px', fontSize: '0.8rem' }}
              >
                {user?.full_name ? user.full_name[0].toUpperCase() : 'F'}
              </div>
              <span className="d-none d-sm-inline fw-semibold small">{user?.full_name}</span>
            </button>
            <ul className="dropdown-menu dropdown-menu-end shadow-sm" style={{ minWidth: '180px' }}>
              <li className="px-3 py-2 border-bottom">
                <p className="mb-0 fw-bold small text-truncate">{user?.full_name}</p>
                <small className="text-muted text-capitalize">{user?.role} • {user?.district || 'India'}</small>
              </li>
              <li>
                <Link className="dropdown-item py-2" to="/profile">
                  <i className="bi bi-person me-2"></i> {t('nav.profile')}
                </Link>
              </li>
              {isAdmin && (
                <li>
                  <Link className="dropdown-item py-2 text-danger fw-semibold" to="/admin">
                    <i className="bi bi-speedometer2 me-2"></i> {t('nav.admin')}
                  </Link>
                </li>
              )}
              <li><hr className="dropdown-divider my-1" /></li>
              <li>
                <button className="dropdown-item py-2 text-danger" onClick={handleLogout}>
                  <i className="bi bi-box-arrow-right me-2"></i> {t('nav.logout')}
                </button>
              </li>
            </ul>
          </div>
        ) : (
          <div className="d-flex align-items-center gap-2">
            <Link to="/login" className="btn btn-sm btn-outline-success">
              {t('nav.login')}
            </Link>
            <Link to="/register" className="btn btn-sm btn-agri">
              {t('nav.register')}
            </Link>
          </div>
        )}
      </div>
    </header>
  );
};

export default Navbar;
