import React, { useState, useEffect } from 'react';
import { marketService } from '../services/marketService';
import { useLanguage } from '../context/LanguageContext';
import LoadingSpinner from '../components/LoadingSpinner';

const MarketPrices = () => {
  const { t } = useLanguage();

  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedState, setSelectedState] = useState('');

  const fetchPrices = async () => {
    setLoading(true);
    try {
      const filters = {};
      if (search) filters.commodity = search;
      if (selectedState) filters.state = selectedState;
      const data = await marketService.getPrices(filters);
      if (data.success) {
        setPrices(data.prices || []);
      }
    } catch (err) {
      console.warn('Error fetching market rates:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrices();
  }, [selectedState]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchPrices();
  };

  return (
    <div className="page-body">
      <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
        <div>
          <h2 className="brand-font mb-1">{t('market.title')}</h2>
          <p className="text-muted small mb-0">{t('market.subtitle')}</p>
        </div>

        {/* Search & State Filter */}
        <form onSubmit={handleSearchSubmit} className="d-flex gap-2">
          <input
            type="text"
            className="form-control form-control-sm"
            placeholder={t('market.search_placeholder')}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ maxWidth: '200px' }}
          />

          <select
            className="form-select form-select-sm"
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            style={{ maxWidth: '170px' }}
          >
            <option value="">All States</option>
            <option value="Andhra Pradesh">Andhra Pradesh</option>
            <option value="Telangana">Telangana</option>
            <option value="Maharashtra">Maharashtra</option>
            <option value="Karnataka">Karnataka</option>
            <option value="Punjab">Punjab</option>
          </select>

          <button type="submit" className="btn btn-sm btn-agri">
            <i className="bi bi-search"></i>
          </button>
        </form>
      </div>

      {loading ? (
        <LoadingSpinner text="Retrieving live APMC Mandi price records..." />
      ) : (
        <div className="agri-card p-0 overflow-hidden shadow-sm">
          <div className="table-responsive">
            <table className="table table-hover align-middle mb-0">
              <thead className="table-light small text-uppercase">
                <tr>
                  <th className="ps-4">Mandi Market</th>
                  <th>State</th>
                  <th>Commodity</th>
                  <th>Variety</th>
                  <th className="text-end">{t('market.min_price')}</th>
                  <th className="text-end">{t('market.max_price')}</th>
                  <th className="text-end">{t('market.modal_price')}</th>
                  <th className="text-center">Trend</th>
                  <th className="pe-4 text-end">{t('market.date')}</th>
                </tr>
              </thead>
              <tbody>
                {prices.length > 0 ? (
                  prices.map((item, idx) => (
                    <tr key={idx}>
                      <td className="ps-4 fw-bold">
                        <i className="bi bi-shop me-2 text-success"></i>
                        {item.market_name}
                        <small className="d-block text-muted fw-normal">{item.district || 'Mandi'}</small>
                      </td>
                      <td className="small text-muted">{item.state}</td>
                      <td>
                        <span className="badge badge-pill-soft badge-soft-emerald">
                          {item.commodity}
                        </span>
                      </td>
                      <td className="small">{item.variety || 'Standard'}</td>
                      <td className="text-end small text-muted">₹{item.min_price}</td>
                      <td className="text-end small text-muted">₹{item.max_price}</td>
                      <td className="text-end fw-bold text-success fs-6">₹{item.modal_price}</td>
                      <td className="text-center">
                        <span className={`badge ${item.price_trend === 'UP' ? 'bg-success' : 'bg-secondary'} small`}>
                          {item.price_trend === 'UP' ? '▲ Rising' : '▼ Steady'}
                        </span>
                      </td>
                      <td className="pe-4 text-end small text-muted">
                        {item.date || 'Today'}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="9" className="text-center py-5 text-muted">
                      No market records found matching your filters.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default MarketPrices;
