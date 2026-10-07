import api from './api';

export const notificationService = {
  // Fetch in-app notifications
  getNotifications: async () => {
    const res = await api.get('/notifications');
    return res.data;
  },

  // Mark single notification as read
  markAsRead: async (notificationId) => {
    const res = await api.put(`/notifications/${notificationId}/read`);
    return res.data;
  },

  // Mark all notifications as read
  markAllRead: async () => {
    const res = await api.put('/notifications/mark-all-read');
    return res.data;
  }
};
