import React, { useState, useEffect } from 'react';
import { notificationService } from '../services/notificationService';
import { useLanguage } from '../context/LanguageContext';
import LoadingSpinner from '../components/LoadingSpinner';

const Notifications = () => {
  const { t } = useLanguage();

  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);

  // Default sample notifications if db is freshly seeded
  const defaultNotifications = [
    {
      id: 1,
      title: 'Monsoon Sowing Window Active',
      message: 'Optimal soil moisture and rainfall recorded in Guntur district. Recommended time to initiate Kharif rice transplanting.',
      type: 'info',
      is_read: false,
      created_at: new Date().toISOString()
    },
    {
      id: 2,
      title: 'High Pest Activity Notice',
      message: 'Spotted bollworm activity reported in neighboring cotton fields. Check pheromone traps daily.',
      type: 'warning',
      is_read: false,
      created_at: new Date(Date.now() - 86400000).toISOString()
    },
    {
      id: 3,
      title: 'APMC Cotton Price Alert',
      message: 'Modal rate for Medium Staple Cotton rose to ₹7,250/Quintal in Kurnool Mandi.',
      type: 'success',
      is_read: true,
      created_at: new Date(Date.now() - 172800000).toISOString()
    }
  ];

  const fetchNotifications = async () => {
    try {
      const data = await notificationService.getNotifications();
      if (data.success && data.notifications && data.notifications.length > 0) {
        setNotifications(data.notifications);
        setUnreadCount(data.unread_count || 0);
      } else {
        setNotifications(defaultNotifications);
        setUnreadCount(2);
      }
    } catch {
      setNotifications(defaultNotifications);
      setUnreadCount(2);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  const handleMarkAsRead = async (id) => {
    try {
      await notificationService.markAsRead(id);
      setNotifications(prev =>
        prev.map(n => (n.id === id ? { ...n, is_read: true } : n))
      );
      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch {
      // Local UI update fallback
      setNotifications(prev =>
        prev.map(n => (n.id === id ? { ...n, is_read: true } : n))
      );
      setUnreadCount(prev => Math.max(0, prev - 1));
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await notificationService.markAllRead();
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
      setUnreadCount(0);
    } catch {
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
      setUnreadCount(0);
    }
  };

  return (
    <div className="page-body">
      <div className="d-flex flex-column flex-sm-row justify-content-between align-items-sm-center gap-3 mb-4">
        <div>
          <h2 className="brand-font mb-1">{t('nav.notifications')}</h2>
          <p className="text-muted small mb-0">Agro-meteorological warnings, market price updates, and advisory alerts</p>
        </div>

        {unreadCount > 0 && (
          <button type="button" className="btn btn-outline-success btn-sm" onClick={handleMarkAllRead}>
            <i className="bi bi-check-all me-1"></i> Mark All as Read
          </button>
        )}
      </div>

      {loading ? (
        <LoadingSpinner text="Retrieving notification inbox..." />
      ) : (
        <div className="agri-card p-0 shadow-sm overflow-hidden">
          <div className="list-group list-group-flush">
            {notifications.length > 0 ? (
              notifications.map((n) => (
                <div
                  key={n.id}
                  className={`list-group-item p-3 d-flex align-items-start gap-3 ${
                    !n.is_read ? 'bg-light bg-opacity-75' : ''
                  }`}
                >
                  <div
                    className={`rounded p-2 text-white flex-shrink-0 ${
                      n.type === 'warning'
                        ? 'bg-warning text-dark'
                        : n.type === 'danger'
                        ? 'bg-danger'
                        : 'bg-success'
                    }`}
                  >
                    <i className="bi bi-bell-fill"></i>
                  </div>

                  <div className="flex-grow-1">
                    <div className="d-flex justify-content-between align-items-center">
                      <h6 className="fw-bold text-dark mb-1 small">{n.title}</h6>
                      <small className="text-muted" style={{ fontSize: '0.75rem' }}>
                        {new Date(n.created_at).toLocaleDateString()}
                      </small>
                    </div>
                    <p className="small text-muted mb-0">{n.message}</p>
                  </div>

                  {!n.is_read && (
                    <button
                      className="btn btn-sm btn-link text-success p-0 flex-shrink-0"
                      title="Mark as read"
                      onClick={() => handleMarkAsRead(n.id)}
                    >
                      <i className="bi bi-check-circle fs-5"></i>
                    </button>
                  )}
                </div>
              ))
            ) : (
              <div className="text-center py-5 text-muted">
                <i className="bi bi-bell-slash fs-3 d-block mb-2"></i>
                No notifications in your inbox.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Notifications;
