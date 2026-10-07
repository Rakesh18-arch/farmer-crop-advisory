import React, { useState, useEffect } from 'react';
import { advisoryService } from '../services/advisoryService';
import { useLanguage } from '../context/LanguageContext';
import LoadingSpinner from '../components/LoadingSpinner';

const PestAdvisory = () => {
  const { t } = useLanguage();

  const [selectedCrop, setSelectedCrop] = useState('');
  const [pests, setPests] = useState([]);
  const [loading, setLoading] = useState(true);

  // Baseline knowledge base pests
  const defaultPests = [
    {
      crop: 'Cotton',
      pest_name: 'Pink Bollworm (Pectinophora gossypiella)',
      damage_symptoms: 'Rosetted flowers, exit holes in bolls, stained lint, premature boll opening.',
      etl: '8 moths/trap/night for 3 consecutive days or 10% damaged green bolls.',
      bio_control: 'Install pheromone traps @ 5/acre. Release Trichogramma bactrae egg parasitoids @ 60,000/acre.',
      chemical_control: 'Spray Emamectin Benzoate 5% SG @ 4g/10L water or Chlorantraniliprole 18.5% SC @ 3ml/10L water.'
    },
    {
      crop: 'Rice',
      pest_name: 'Yellow Stem Borer (Scirpophaga incertulas)',
      damage_symptoms: 'Dead hearts at tillering stage and white ears with empty grains at panicle stage.',
      etl: '2 egg masses/sq.m or 5% dead hearts.',
      bio_control: 'Install bird perches @ 20/acre. Release Trichogramma japonicum parasitoids.',
      chemical_control: 'Apply Cartap Hydrochloride 4G @ 10 kg/acre or Chlorantraniliprole 0.4% G in soil.'
    },
    {
      crop: 'Tomato',
      pest_name: 'Fruit Borer (Helicoverpa armigera)',
      damage_symptoms: 'Circular bore holes on green and ripe fruits, internal pulp consumption.',
      etl: '1 larva/plant or 5% fruit damage.',
      bio_control: 'Plant marigold as trap crop (1 row for every 16 tomato rows). Spray HaNPV 250 LE/acre.',
      chemical_control: 'Spray Flubendiamide 39.35% SC @ 2.5 ml/10L water with 7-day pre-harvest interval.'
    },
    {
      crop: 'Maize',
      pest_name: 'Fall Armyworm (Spodoptera frugiperda)',
      damage_symptoms: 'Shot holes on leaves, whorl damage, sawdust-like fecal matter inside whorl.',
      etl: '5% damaged seedlings or 10% damaged whorls.',
      bio_control: 'Whorl application of dry sand or neem seed kernel extract (NSKE 5%). Release Nomuraea rileyi.',
      chemical_control: 'Spray Spinetoram 11.7% SC @ 5 ml/10L water directed into plant whorls.'
    },
    {
      crop: 'Chilli',
      pest_name: 'Chilli Thrips (Scirtothrips dorsalis)',
      damage_symptoms: 'Upward leaf curling, boat-shaped leaves, bronzing on leaf undersides.',
      etl: '2 thrips/leaf.',
      bio_control: 'Install blue sticky traps @ 10/acre. Spray neem oil (10,000 ppm) @ 3 ml/L.',
      chemical_control: 'Spray Fipronil 5% SC @ 2 ml/L or Diafenthiuron 50% WP @ 1.2 g/L.'
    }
  ];

  useEffect(() => {
    const fetchPests = async () => {
      try {
        const data = await advisoryService.getPestAdvisories(selectedCrop);
        if (data.success && data.pests && data.pests.length > 0) {
          setPests(data.pests);
        } else {
          setPests(defaultPests);
        }
      } catch {
        setPests(defaultPests);
      } finally {
        setLoading(false);
      }
    };

    fetchPests();
  }, [selectedCrop]);

  const filteredPests = selectedCrop
    ? pests.filter(p => p.crop.toLowerCase() === selectedCrop.toLowerCase())
    : pests;

  return (
    <div className="page-body">
      <div className="d-flex flex-column flex-sm-row justify-content-between align-items-sm-center gap-3 mb-4">
        <div>
          <h2 className="brand-font mb-1">{t('nav.pest_advisory')}</h2>
          <p className="text-muted small mb-0">Integrated Pest Management (IPM) guidelines, economic threshold levels, and biological controls</p>
        </div>

        {/* Crop Filter Dropdown */}
        <select
          className="form-select form-select-sm"
          style={{ maxWidth: '220px' }}
          value={selectedCrop}
          onChange={(e) => setSelectedCrop(e.target.value)}
        >
          <option value="">All Crop Pests</option>
          <option value="Cotton">Cotton</option>
          <option value="Rice">Rice (Paddy)</option>
          <option value="Tomato">Tomato</option>
          <option value="Maize">Maize</option>
          <option value="Chilli">Chilli</option>
        </select>
      </div>

      {loading ? (
        <LoadingSpinner text="Retrieving Integrated Pest Management guidelines..." />
      ) : (
        <div className="row g-4">
          {filteredPests.map((pest, idx) => (
            <div key={idx} className="col-12 col-lg-6">
              <div className="agri-card p-4 h-100 shadow-sm border">
                <div className="d-flex justify-content-between align-items-start mb-2">
                  <span className="badge badge-pill-soft badge-soft-emerald">
                    Crop: {pest.crop}
                  </span>
                  <span className="badge bg-danger text-white small">IPM Protocol</span>
                </div>

                <h5 className="brand-font text-dark fw-bold mb-2">{pest.pest_name}</h5>

                <div className="mb-3">
                  <small className="fw-bold text-muted d-block">Damage Symptoms:</small>
                  <p className="small text-muted mb-0">{pest.damage_symptoms}</p>
                </div>

                <div className="p-2 rounded bg-light border mb-3">
                  <small className="fw-bold text-dark d-block">Economic Threshold Level (ETL):</small>
                  <small className="text-danger fw-semibold">{pest.etl}</small>
                </div>

                <div className="p-3 rounded border mb-2" style={{ backgroundColor: '#f0fdf4' }}>
                  <h6 className="fw-bold text-success mb-1 small">
                    <i className="bi bi-shield-check me-1"></i> Biological & Cultural Control
                  </h6>
                  <p className="small text-muted mb-0">{pest.bio_control}</p>
                </div>

                <div className="p-3 rounded border" style={{ backgroundColor: '#fff7ed' }}>
                  <h6 className="fw-bold text-warning mb-1 small">
                    <i className="bi bi-radioactive me-1"></i> Recommended Chemical Intervention
                  </h6>
                  <p className="small text-muted mb-0">{pest.chemical_control}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PestAdvisory;
