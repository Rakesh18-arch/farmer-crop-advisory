import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';

const Sidebar = ({ isOpen, onClose }) => {
  const { isAdmin } = useAuth();
  const { t } = useLanguage();

  return (
    <aside className={`sidebar ${isOpen ? 'show' : ''}`}>
      {/* Brand Header */}
      <div className="sidebar-brand">
        <div className="sidebar-brand-icon">
          <span>🌱</span>
        </div>
        <div className="d-flex flex-column">
          <span className="brand-font fs-6 fw-bold text-white lh-1">AgriAdvisory</span>
          <small className="text-emerald-400 text-muted" style={{ fontSize: '0.72rem' }}>AI Decision System</small>
        </div>
      </div>

      {/* Navigation Links */}
      <ul className="sidebar-nav">
        <li className="sidebar-category">Overview</li>
        <li>
          <NavLink to="/" end className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-grid-1x2"></i>
            <span>{t('nav.dashboard')}</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/profile" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-person-badge"></i>
            <span>{t('nav.profile')}</span>
          </NavLink>
        </li>

        <li className="sidebar-category">Advisory Engine</li>
        <li>
          <NavLink to="/crop-recommendation" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-flower1"></i>
            <span>{t('nav.crop_advisory')}</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/soil-analysis" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-droplet-half"></i>
            <span>{t('nav.soil_analysis')}</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/weather" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-cloud-sun"></i>
            <span>{t('nav.weather')}</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/irrigation" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-moisture"></i>
            <span>{t('nav.irrigation')}</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/fertilizer" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-calculator"></i>
            <span>{t('nav.fertilizer')}</span>
          </NavLink>
        </li>

        <li className="sidebar-category">Protection & Market</li>
        <li>
          <NavLink to="/disease-detection" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-camera"></i>
            <span>{t('nav.disease_detection')}</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/pest-advisory" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-bug"></i>
            <span>{t('nav.pest_advisory')}</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/market-prices" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-graph-up-arrow"></i>
            <span>{t('nav.market_prices')}</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/schemes" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-award"></i>
            <span>{t('nav.schemes')}</span>
          </NavLink>
        </li>

        <li className="sidebar-category">Planning & AI</li>
        <li>
          <NavLink to="/crop-calendar" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-calendar-event"></i>
            <span>{t('nav.calendar')}</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/yield-prediction" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-pie-chart"></i>
            <span>{t('nav.yield_prediction')}</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/chatbot" className={({ isActive }) => `nav-item-link ${isActive ? 'active' : ''}`} onClick={onClose}>
            <i className="bi bi-chat-dots"></i>
            <span>{t('nav.chatbot')}</span>
          </NavLink>
        </li>

        {isAdmin && (
          <>
            <li className="sidebar-category text-warning">Administration</li>
            <li>
              <NavLink to="/admin" className={({ isActive }) => `nav-item-link text-warning ${isActive ? 'active' : ''}`} onClick={onClose}>
                <i className="bi bi-shield-lock"></i>
                <span>{t('nav.admin')}</span>
              </NavLink>
            </li>
          </>
        )}
      </ul>
    </aside>
  );
};

export default Sidebar;
