import api from './api';

export const diseaseService = {
  // Detect disease by uploading image
  detectDisease: async (file, cropHint = '') => {
    const formData = new FormData();
    formData.append('image', file);
    if (cropHint) {
      formData.append('crop_hint', cropHint);
    }

    const res = await api.post('/disease/detect', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return res.data;
  },

  // Get master disease catalog
  getDiseasesCatalog: async (crop = '') => {
    const params = crop ? { crop } : {};
    const res = await api.get('/disease/catalog', { params });
    return res.data;
  },

  // Get single disease detail
  getDiseaseDetails: async (diseaseId) => {
    const res = await api.get(`/disease/${diseaseId}`);
    return res.data;
  }
};
