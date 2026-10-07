import api from './api';

export const marketService = {
  // Get APMC live mandi prices
  getPrices: async (filters = {}) => {
    const res = await api.get('/market/prices', { params: filters });
    return res.data;
  },

  // Get distinct commodities list
  getCommodities: async () => {
    const res = await api.get('/market/commodities');
    return res.data;
  },

  // Get nearby markets based on coordinates or district
  getNearbyMarkets: async (lat, lon, state = '') => {
    const res = await api.get('/market/nearby', {
      params: { lat, lon, state }
    });
    return res.data;
  }
};
