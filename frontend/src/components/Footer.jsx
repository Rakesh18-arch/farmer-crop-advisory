import React from 'react';

const Footer = () => {
  return (
    <footer className="py-3 px-4 bg-white border-top text-muted small mt-auto">
      <div className="d-flex flex-column flex-md-row justify-content-between align-items-center gap-2">
        <div>
          <span>© 2026 <strong>Farmer Crop Advisory Platform</strong>. Built for Indian Agricultural Ecosystem.</span>
        </div>
        <div className="d-flex align-items-center gap-3">
          <span className="badge badge-pill-soft badge-soft-emerald">
            <i className="bi bi-cpu"></i> AI Powered v1.0
          </span>
          <span>Data: ICAR • IMD • Agmarknet APMC</span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
