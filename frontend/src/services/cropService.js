import api from './api';

export const cropService = {
  // Get master crop list
  getCrops: async (category = '') => {
    const params = category ? { category } : {};
    const res = await api.get('/crop/list', { params });
    return res.data;
  },

  // Get single crop details
  getCropById: async (cropId) => {
    const res = await api.get(`/crop/${cropId}`);
    return res.data;
  },

  // Filter crops by season
  getCropsBySeason: async (season = 'Kharif') => {
    const res = await api.get('/crop/seasonal', { params: { season } });
    return res.data;
  },

  // Get AI Crop Recommendation
  recommendCrop: async (parameters) => {
    const res = await api.post('/crop/recommend', parameters);
    return res.data;
  },

  // Get deep LLM agronomic explanation for recommended crop
  explainRecommendation: async (payload) => {
    const res = await api.post('/crop/explain-recommendation', payload);
    return res.data;
  },

  // Get recommendation history for authenticated farmer
  getHistory: async () => {
    const res = await api.get('/crop/recommendations/history');
    return res.data;
  },

  // Get stage-wise crop calendar
  getCalendar: async (cropName = 'Rice') => {
    const res = await api.get('/crop/calendar', { params: { crop: cropName } });
    return res.data;
  },

  // Harvest Yield Prediction AI
  predictYield: async (parameters) => {
    const res = await api.post('/crop/predict-yield', parameters);
    return res.data;
  }
};
