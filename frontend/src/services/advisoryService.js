import api from './api';

export const advisoryService = {
  // Fertilizer NPK deficit and organic calculator
  calculateFertilizer: async (data) => {
    const res = await api.post('/fertilizer/calculate', data);
    return res.data;
  },

  // Smart irrigation schedule based on soil, crop stage, and weather
  getIrrigationSchedule: async (data) => {
    const res = await api.post('/irrigation/schedule', data);
    return res.data;
  },

  // Disease & Pest Advisory
  getPestAdvisories: async (crop = '') => {
    const params = crop ? { crop } : {};
    const res = await api.get('/disease/pests', { params });
    return res.data;
  }
};
