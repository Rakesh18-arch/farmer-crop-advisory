import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { cropService } from '../services/cropService';
import { useLanguage } from '../context/LanguageContext';
import LoadingSpinner from '../components/LoadingSpinner';

const CropCalendar = () => {
  const { t } = useLanguage();
  const [searchParams] = useSearchParams();

  const initialCrop = searchParams.get('crop') || 'Rice';
  const [selectedCrop, setSelectedCrop] = useState(initialCrop);
  const [calendarData, setCalendarData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Default stage templates
  const defaultCalendars = {
    Rice: {
      duration_days: 125,
      stages: [
        {
          stage_name: 'Land Preparation & Nursery Sowing',
          days: 'Days 0 - 20',
          tasks: 'Puddle field thoroughly. Apply 2 tons FYM per acre. Prepare raised nursery beds and treat seed with Carbendazim.',
          water_need: 'Keep nursery bed moist. Saturate main field 2 days prior to transplanting.'
        },
        {
          stage_name: 'Seedling Transplanting',
          days: 'Days 21 - 28',
          tasks: 'Transplant 21-day-old seedlings with 2-3 seedlings per hill at 20x15 cm spacing. Apply basal dose DAP (75kg) and MOP (50kg).',
          water_need: 'Maintain 2 cm standing water layer.'
        },
        {
          stage_name: 'Tillering & Vegetative Phase',
          days: 'Days 29 - 60',
          tasks: 'First split of Urea (40 kg/acre). Hand weeding or apply bispyribac-sodium. Monitor for leaf folder.',
          water_need: 'Maintain shallow water layer of 3-5 cm. Drain field for 2 days at maximum tillering.'
        },
        {
          stage_name: 'Panicle Initiation & Flowering',
          days: 'Days 61 - 90',
          tasks: 'Second split of Urea (40 kg/acre). Inspect for Yellow Stem Borer and Brown Planthopper (BPH). Spray Cartap if ETL exceeded.',
          water_need: 'Critical moisture stage! Continuous 5 cm water depth essential to avoid grain sterility.'
        },
        {
          stage_name: 'Maturity & Harvest',
          days: 'Days 91 - 125',
          tasks: 'Withhold irrigation 10 days prior to harvest. Harvest when 80-85% grains turn golden yellow. Sun-dry to 14% moisture.',
          water_need: 'Complete field drainage 7-10 days before harvesting.'
        }
      ]
    },
    Cotton: {
      duration_days: 160,
      stages: [
        {
          stage_name: 'Field Preparation & Sowing',
          days: 'Days 0 - 15',
          tasks: 'Deep summer ploughing. Form ridges and furrows at 90x60 cm. Sow delinted seeds treated with Imidacloprid.',
          water_need: 'Irrigate immediately after dibbling seeds on ridge flanks.'
        },
        {
          stage_name: 'Vegetative & Square Formation',
          days: 'Days 16 - 60',
          tasks: 'Thinning to single plant per hill at 15 DAS. Top-dress 30 kg Nitrogen. Monitor for sucking pests (thrips, aphids).',
          water_need: 'Irrigate at 12-15 day intervals depending on rainfall.'
        },
        {
          stage_name: 'Flowering & Boll Development',
          days: 'Days 61 - 110',
          tasks: 'Foliar spray of 2% DAP or Potassium Nitrate for boll retention. Install pheromone traps for pink bollworm.',
          water_need: 'Critical watering stage. Prevent soil cracking to avert boll dropping.'
        },
        {
          stage_name: 'Boll Bursting & Picking',
          days: 'Days 111 - 160',
          tasks: 'Pick clean, fully burst bolls in dry sunny morning hours. Avoid mixing stained or trash-laden cotton.',
          water_need: 'Stop irrigation when 30% bolls burst.'
        }
      ]
    }
  };

  useEffect(() => {
    const fetchCalendar = async () => {
      setLoading(true);
      try {
        const data = await cropService.getCalendar(selectedCrop);
        if (data.success && data.calendar) {
          setCalendarData(data.calendar);
        } else {
          setCalendarData(defaultCalendars[selectedCrop] || defaultCalendars.Rice);
        }
      } catch {
        setCalendarData(defaultCalendars[selectedCrop] || defaultCalendars.Rice);
      } finally {
        setLoading(false);
      }
    };

    fetchCalendar();
  }, [selectedCrop]);

  return (
    <div className="page-body">
      <div className="d-flex flex-column flex-sm-row justify-content-between align-items-sm-center gap-3 mb-4">
        <div>
          <h2 className="brand-font mb-1">{t('nav.calendar')}</h2>
          <p className="text-muted small mb-0">Phase-by-phase agronomic timeline, critical irrigation events, and nutrient scheduling</p>
        </div>

        <select
          className="form-select form-select-sm"
          style={{ maxWidth: '200px' }}
          value={selectedCrop}
          onChange={(e) => setSelectedCrop(e.target.value)}
        >
          <option value="Rice">Rice (Paddy)</option>
          <option value="Cotton">Cotton</option>
          <option value="Wheat">Wheat</option>
          <option value="Maize">Maize</option>
          <option value="Tomato">Tomato</option>
        </select>
      </div>

      {loading ? (
        <LoadingSpinner text="Compiling stage-by-stage agronomic planner..." />
      ) : (
        <div className="agri-card p-4">
          <div className="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom">
            <div>
              <h4 className="brand-font text-success mb-1">{selectedCrop} Agronomic Lifecycle</h4>
              <span className="text-muted small">Total Growth Duration: ~{calendarData?.duration_days || 120} Days</span>
            </div>
            <span className="badge badge-pill-soft badge-soft-emerald">ICAR Agronomic Standard</span>
          </div>

          {/* Timeline Stages */}
          <div className="timeline">
            {calendarData?.stages?.map((stage, idx) => (
              <div key={idx} className="mb-4 pb-3 border-bottom position-relative ps-4">
                {/* Circle badge */}
                <div
                  className="position-absolute start-0 top-0 bg-success text-white rounded-circle d-flex align-items-center justify-content-center fw-bold"
                  style={{ width: '26px', height: '26px', fontSize: '0.8rem' }}
                >
                  {idx + 1}
                </div>

                <div className="d-flex flex-column flex-sm-row justify-content-between align-items-sm-center mb-2">
                  <h6 className="brand-font text-dark fw-bold mb-0">{stage.stage_name}</h6>
                  <span className="badge bg-light text-dark border small mt-1 mt-sm-0">{stage.days}</span>
                </div>

                <div className="row g-2 mt-1">
                  <div className="col-12 col-md-7">
                    <small className="fw-semibold text-dark d-block">Recommended Agronomic Tasks:</small>
                    <p className="small text-muted mb-0">{stage.tasks}</p>
                  </div>
                  <div className="col-12 col-md-5">
                    <small className="fw-semibold text-info d-block">Water & Moisture Requirement:</small>
                    <p className="small text-muted mb-0">{stage.water_need}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CropCalendar;
