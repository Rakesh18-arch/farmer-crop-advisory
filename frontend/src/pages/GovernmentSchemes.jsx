import React, { useState, useEffect } from 'react';
import { schemeService } from '../services/schemeService';
import { useLanguage } from '../context/LanguageContext';
import LoadingSpinner from '../components/LoadingSpinner';

const GovernmentSchemes = () => {
  const { t } = useLanguage();

  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('');

  // Built-in schemes fallback
  const defaultSchemes = [
    {
      scheme_name: 'PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)',
      category: 'Income Support',
      description: 'Direct income support of ₹6,000 per year in 3 equal installments of ₹2,000 to all land-holding farmer families.',
      financial_benefit: '₹6,000 / Year (₹2,000 every 4 months via Direct Benefit Transfer DBT)',
      eligibility: 'All landholding farmer families with cultivable land in their names.',
      required_documents: 'Aadhaar Card, Land ownership papers (Pattadar Passbook / RoR), Bank Account linked with Aadhaar.',
      official_portal_url: 'https://pmkisan.gov.in'
    },
    {
      scheme_name: 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
      category: 'Crop Insurance',
      description: 'Comprehensive risk insurance covering yield losses due to non-preventable natural risks (drought, flood, pests, hailstorm).',
      financial_benefit: 'Subsidized premium: 2% for Kharif crops, 1.5% for Rabi crops, 5% for commercial/horticultural crops.',
      eligibility: 'All farmers growing notified crops in notified areas (both loanee and non-loanee farmers).',
      required_documents: 'Aadhaar, Sowing Certificate / Vahan record, Bank Passbook, Land Revenue records.',
      official_portal_url: 'https://pmfby.gov.in'
    },
    {
      scheme_name: 'Soil Health Card Scheme',
      category: 'Soil & Inputs',
      description: 'Issues soil health cards every 2 years containing nutrient status (12 parameters: N, P, K, S, Zn, Fe, Cu, Mn, Bo, pH, EC, OC) with dosage recommendations.',
      financial_benefit: '100% Free soil testing and personalized nutrient management prescription booklet.',
      eligibility: 'All agricultural landowners and cultivating tenant farmers.',
      required_documents: 'Farmer identification, GPS coordinates of soil sample plot.',
      official_portal_url: 'https://soilhealth.dac.gov.in'
    },
    {
      scheme_name: 'Rythu Bandhu / YSR Rythu Bharosa',
      category: 'State Welfare',
      description: 'State government investment support to relieve farmers from debt burden and support input purchases (seeds, fertilizers, pesticides).',
      financial_benefit: '₹10,000 - ₹13,500 per acre per year direct payment.',
      eligibility: 'Resident farmers possessing agricultural land in Andhra Pradesh / Telangana.',
      required_documents: 'Pattadar Passbook, Aadhaar, Active Bank Account details.',
      official_portal_url: 'https://ysrrythubharosa.ap.gov.in'
    },
    {
      scheme_name: 'Paramparagat Krishi Vikas Yojana (PKVY)',
      category: 'Organic Farming',
      description: 'Promotes organic farming through cluster approach and Participatory Guarantee System (PGS) certification.',
      financial_benefit: 'Financial assistance of ₹50,000 per hectare for 3 years (₹31,000 for organic inputs).',
      eligibility: 'Farmers willing to form clusters of 50 or more acres and adopt chemical-free practices.',
      required_documents: 'Aadhaar Card, Cluster registration agreement.',
      official_portal_url: 'https://pgsindia-ncof.gov.in'
    }
  ];

  useEffect(() => {
    const fetchSchemes = async () => {
      try {
        const data = await schemeService.getSchemes(selectedCategory);
        if (data.success && data.schemes && data.schemes.length > 0) {
          setSchemes(data.schemes);
        } else {
          setSchemes(defaultSchemes);
        }
      } catch {
        setSchemes(defaultSchemes);
      } finally {
        setLoading(false);
      }
    };

    fetchSchemes();
  }, [selectedCategory]);

  const filteredSchemes = selectedCategory
    ? schemes.filter(s => s.category?.toLowerCase().includes(selectedCategory.toLowerCase()))
    : schemes;

  return (
    <div className="page-body">
      <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
        <div>
          <h2 className="brand-font mb-1">{t('nav.schemes')}</h2>
          <p className="text-muted small mb-0">Central and State Government agricultural welfare subsidies, financial incentives, and portals</p>
        </div>

        {/* Category Pills */}
        <div className="btn-group btn-group-sm">
          <button className={`btn ${selectedCategory === '' ? 'btn-success' : 'btn-outline-secondary'}`} onClick={() => setSelectedCategory('')}>All Schemes</button>
          <button className={`btn ${selectedCategory === 'Income' ? 'btn-success' : 'btn-outline-secondary'}`} onClick={() => setSelectedCategory('Income')}>Income Support</button>
          <button className={`btn ${selectedCategory === 'Insurance' ? 'btn-success' : 'btn-outline-secondary'}`} onClick={() => setSelectedCategory('Insurance')}>Insurance</button>
          <button className={`btn ${selectedCategory === 'Organic' ? 'btn-success' : 'btn-outline-secondary'}`} onClick={() => setSelectedCategory('Organic')}>Organic</button>
        </div>
      </div>

      {loading ? (
        <LoadingSpinner text="Retrieving government agricultural subsidy catalogs..." />
      ) : (
        <div className="row g-4">
          {filteredSchemes.map((scheme, idx) => (
            <div key={idx} className="col-12 col-lg-6">
              <div className="agri-card p-4 h-100 shadow-sm d-flex flex-column">
                <div className="d-flex justify-content-between align-items-start mb-2">
                  <span className="badge badge-pill-soft badge-soft-emerald">
                    {scheme.category || 'Central Scheme'}
                  </span>
                  <span className="badge bg-light text-dark border small">Government of India</span>
                </div>

                <h5 className="brand-font text-dark fw-bold mb-2">{scheme.scheme_name}</h5>
                <p className="small text-muted mb-3">{scheme.description}</p>

                <div className="p-3 rounded border mb-3" style={{ backgroundColor: '#ecfdf5' }}>
                  <small className="text-uppercase fw-bold text-success d-block">Financial Assistance & Benefits</small>
                  <span className="fw-bold text-dark fs-6">{scheme.financial_benefit}</span>
                </div>

                <div className="mb-2">
                  <small className="fw-bold text-dark d-block">Eligibility:</small>
                  <small className="text-muted">{scheme.eligibility}</small>
                </div>

                <div className="mb-3">
                  <small className="fw-bold text-dark d-block">Required Documents:</small>
                  <small className="text-muted">{scheme.required_documents}</small>
                </div>

                <div className="mt-auto pt-3 border-top">
                  <a
                    href={scheme.official_portal_url || 'https://agricoop.nic.in'}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-outline-success btn-sm w-100 fw-semibold"
                  >
                    <i className="bi bi-box-arrow-up-right me-1"></i> Visit Official Scheme Portal
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GovernmentSchemes;
