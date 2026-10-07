import api from './api';

export const adminService = {
  // Get administrative analytics and metrics
  getStats: async () => {
    const res = await api.get('/admin/stats');
    return res.data;
  },

  // Get paginated farmers list
  getFarmers: async (page = 1, perPage = 15, q = '') => {
    const params = { page, per_page: perPage };
    if (q) params.q = q;
    const res = await api.get('/admin/farmers', { params });
    return res.data;
  },

  // Toggle farmer account active status
  toggleFarmerStatus: async (userId) => {
    const res = await api.put(`/admin/farmers/${userId}/toggle-status`);
    return res.data;
  },

  // Get platform-wide crop recommendations
  getRecommendations: async (page = 1, perPage = 20) => {
    const res = await api.get('/admin/recommendations', {
      params: { page, per_page: perPage }
    });
    return res.data;
  },

  // Download CSV report blob and trigger browser save
  downloadReport: async (reportType) => {
    const res = await api.get(`/admin/reports/${reportType}`, {
      responseType: 'blob'
    });
    const blob = new Blob([res.data], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `report_${reportType}_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
    window.URL.revokeObjectURL(url);
  }
};
