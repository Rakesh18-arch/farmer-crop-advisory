import React, { useState, useEffect } from 'react';
import { adminService } from '../services/adminService';
import { useLanguage } from '../context/LanguageContext';
import AlertCard from '../components/AlertCard';
import LoadingSpinner from '../components/LoadingSpinner';

const AdminDashboard = () => {
  const { t } = useLanguage();

  const [stats, setStats] = useState(null);
  const [farmers, setFarmers] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState('');
  const [message, setMessage] = useState({ text: '', type: '' });

  const loadAdminData = async () => {
    try {
      const [statsData, farmersData] = await Promise.all([
        adminService.getStats(),
        adminService.getFarmers(1, 15, searchQuery)
      ]);

      if (statsData.success) setStats(statsData);
      if (farmersData.success) setFarmers(farmersData.farmers || []);
    } catch (err) {
      setMessage({ text: 'Error fetching administrative analytics.', type: 'danger' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAdminData();
  }, [searchQuery]);

  const handleToggleStatus = async (userId) => {
    try {
      const res = await adminService.toggleFarmerStatus(userId);
      if (res.success) {
        setFarmers(prev =>
          prev.map(f => (f.id === userId ? { ...f, is_active: res.is_active } : f))
        );
        setMessage({ text: res.message, type: 'success' });
      }
    } catch (err) {
      setMessage({ text: err?.response?.data?.message || 'Could not update user status.', type: 'danger' });
    }
  };

  const handleDownloadCsv = async (reportType) => {
    setExporting(reportType);
    try {
      await adminService.downloadReport(reportType);
    } catch (err) {
      setMessage({ text: `Failed to export ${reportType} report.`, type: 'danger' });
    } finally {
      setExporting('');
    }
  };

  if (loading) {
    return <LoadingSpinner text="Loading Administrative platform metrics and user logs..." />;
  }

  return (
    <div className="page-body">
      <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
        <div>
          <h2 className="brand-font mb-1 text-danger">
            <i className="bi bi-shield-lock-fill me-2"></i> {t('nav.admin')}
          </h2>
          <p className="text-muted small mb-0">System administration, telemetry diagnostics, farmer moderation, and CSV exports</p>
        </div>

        <span className="badge bg-danger text-white px-3 py-2 fs-6">
          <i className="bi bi-person-check-fill me-1"></i> Superadmin Active
        </span>
      </div>

      {message.text && (
        <AlertCard type={message.type} title="System Message" message={message.text} />
      )}

      {/* Metric Cards Row */}
      <div className="row g-3 mb-4">
        <div className="col-12 col-sm-6 col-lg-3">
          <div className="agri-stat-card">
            <div className="stat-icon-wrapper stat-icon-emerald">
              <i className="bi bi-people-fill"></i>
            </div>
            <div>
              <div className="stat-value">{stats?.metrics?.total_farmers || 1}</div>
              <div className="stat-label">Registered Farmers</div>
            </div>
          </div>
        </div>

        <div className="col-12 col-sm-6 col-lg-3">
          <div className="agri-stat-card">
            <div className="stat-icon-wrapper stat-icon-blue">
              <i className="bi bi-cpu"></i>
            </div>
            <div>
              <div className="stat-value">{stats?.metrics?.total_recommendations || 0}</div>
              <div className="stat-label">Crop Advisories Run</div>
            </div>
          </div>
        </div>

        <div className="col-12 col-sm-6 col-lg-3">
          <div className="agri-stat-card">
            <div className="stat-icon-wrapper stat-icon-amber">
              <i className="bi bi-camera"></i>
            </div>
            <div>
              <div className="stat-value">{stats?.metrics?.total_disease_scans || 0}</div>
              <div className="stat-label">Leaf Disease Scans</div>
            </div>
          </div>
        </div>

        <div className="col-12 col-sm-6 col-lg-3">
          <div className="agri-stat-card">
            <div className="stat-icon-wrapper stat-icon-purple">
              <i className="bi bi-journal-bookmark-fill"></i>
            </div>
            <div>
              <div className="stat-value">{stats?.metrics?.total_crops_catalog || 12}</div>
              <div className="stat-label">Crop Master Catalog</div>
            </div>
          </div>
        </div>
      </div>

      {/* CSV Export Center Row */}
      <div className="agri-card p-4 mb-4">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h5 className="brand-font mb-0 text-dark">
            <i className="bi bi-file-earmark-spreadsheet-fill text-success me-2"></i> CSV Data Export Center
          </h5>
          <small className="text-muted">Direct database streaming</small>
        </div>
        <p className="text-muted small mb-3">
          Download formatted CSV records for academic reporting, audit compliance, or statistical evaluation.
        </p>

        <div className="d-flex flex-wrap gap-2">
          <button
            type="button"
            className="btn btn-outline-success btn-sm"
            onClick={() => handleDownloadCsv('farmers')}
            disabled={exporting === 'farmers'}
          >
            {exporting === 'farmers' ? <span className="spinner-border spinner-border-sm me-1"></span> : <i className="bi bi-download me-1"></i>}
            Export Farmers CSV
          </button>

          <button
            type="button"
            className="btn btn-outline-success btn-sm"
            onClick={() => handleDownloadCsv('recommendations')}
            disabled={exporting === 'recommendations'}
          >
            {exporting === 'recommendations' ? <span className="spinner-border spinner-border-sm me-1"></span> : <i className="bi bi-download me-1"></i>}
            Export Recommendations CSV
          </button>

          <button
            type="button"
            className="btn btn-outline-success btn-sm"
            onClick={() => handleDownloadCsv('diseases')}
            disabled={exporting === 'diseases'}
          >
            {exporting === 'diseases' ? <span className="spinner-border spinner-border-sm me-1"></span> : <i className="bi bi-download me-1"></i>}
            Export Disease Scans CSV
          </button>

          <button
            type="button"
            className="btn btn-outline-success btn-sm"
            onClick={() => handleDownloadCsv('market_prices')}
            disabled={exporting === 'market_prices'}
          >
            {exporting === 'market_prices' ? <span className="spinner-border spinner-border-sm me-1"></span> : <i className="bi bi-download me-1"></i>}
            Export APMC Mandi Prices CSV
          </button>

          <button
            type="button"
            className="btn btn-outline-success btn-sm"
            onClick={() => handleDownloadCsv('schemes')}
            disabled={exporting === 'schemes'}
          >
            {exporting === 'schemes' ? <span className="spinner-border spinner-border-sm me-1"></span> : <i className="bi bi-download me-1"></i>}
            Export Welfare Schemes CSV
          </button>
        </div>
      </div>

      {/* Registered Farmers Directory */}
      <div className="agri-card p-4">
        <div className="d-flex flex-column flex-sm-row justify-content-between align-items-sm-center gap-3 mb-3">
          <h5 className="brand-font mb-0 text-dark">
            <i className="bi bi-person-lines-fill text-success me-2"></i> Registered Farmers Directory
          </h5>

          <input
            type="text"
            className="form-control form-control-sm"
            placeholder="Search by name, district, or phone..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ maxWidth: '280px' }}
          />
        </div>

        <div className="table-responsive">
          <table className="table table-hover align-middle mb-0">
            <thead className="table-light small text-uppercase">
              <tr>
                <th className="ps-3">Farmer Name</th>
                <th>Contact</th>
                <th>Location</th>
                <th>Land Size</th>
                <th>Soil Type</th>
                <th>Status</th>
                <th className="pe-3 text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              {farmers.length > 0 ? (
                farmers.map((f) => (
                  <tr key={f.id}>
                    <td className="ps-3 fw-bold">
                      <div className="d-flex align-items-center gap-2">
                        <div className="bg-success text-white rounded-circle p-1 small" style={{ width: '28px', height: '28px', textAlign: 'center' }}>
                          {f.full_name[0]}
                        </div>
                        <div>
                          <span>{f.full_name}</span>
                          <small className="d-block text-muted fw-normal">{f.email}</small>
                        </div>
                      </div>
                    </td>
                    <td className="small">{f.phone_number}</td>
                    <td className="small text-muted">{f.district}, {f.state}</td>
                    <td className="small">{f.farm_size ? `${f.farm_size} Acres` : 'N/A'}</td>
                    <td className="small">{f.soil_type || 'Loamy'}</td>
                    <td>
                      <span className={`badge ${f.is_active ? 'bg-success' : 'bg-secondary'} small`}>
                        {f.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="pe-3 text-end">
                      <button
                        className={`btn btn-sm ${f.is_active ? 'btn-outline-danger' : 'btn-outline-success'}`}
                        onClick={() => handleToggleStatus(f.id)}
                      >
                        {f.is_active ? 'Deactivate' : 'Activate'}
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="7" className="text-center py-4 text-muted">
                    No farmer records found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
