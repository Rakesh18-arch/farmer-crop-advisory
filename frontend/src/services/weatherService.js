import api from './api';

export const weatherService = {
  // Current weather with agro-climatic summary
  getCurrentWeather: async (location = 'Guntur', lat = null, lon = null) => {
    const params = { location };
    if (lat && lon) {
      params.lat = lat;
      params.lon = lon;
    }
    const res = await api.get('/weather/current', { params });
    return res.data;
  },

  // 5-day agricultural weather forecast
  getForecast: async (location = 'Guntur') => {
    const res = await api.get('/weather/forecast', { params: { location } });
    return res.data;
  },

  // Agricultural specific advisories (e.g., spray window, frost, heatwave)
  getAgriculturalAdvisories: async (location = 'Guntur') => {
    const res = await api.get('/weather/advisories', { params: { location } });
    return res.data;
  }
};
