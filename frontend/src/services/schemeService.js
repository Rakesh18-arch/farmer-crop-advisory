import api from './api';

export const schemeService = {
  // Get government agricultural welfare schemes
  getSchemes: async (category = '', state = '') => {
    const params = {};
    if (category) params.category = category;
    if (state) params.state = state;
    const res = await api.get('/schemes/list', { params });
    return res.data;
  },

  // Get specific scheme details
  getSchemeById: async (schemeId) => {
    const res = await api.get(`/schemes/${schemeId}`);
    return res.data;
  }
};
