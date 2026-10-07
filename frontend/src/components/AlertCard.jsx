import React from 'react';

const AlertCard = ({ type = 'info', title, message, icon }) => {
  const typeMap = {
    warning: {
      border: '#f59e0b',
      bg: '#fffbeb',
      textColor: '#92400e',
      defaultIcon: 'bi-exclamation-triangle-fill'
    },
    danger: {
      border: '#ef4444',
      bg: '#fef2f2',
      textColor: '#991b1b',
      defaultIcon: 'bi-shield-exclamation'
    },
    success: {
      border: '#10b981',
      bg: '#ecfdf5',
      textColor: '#065f46',
      defaultIcon: 'bi-check-circle-fill'
    },
    info: {
      border: '#3b82f6',
      bg: '#eff6ff',
      textColor: '#1e40af',
      defaultIcon: 'bi-info-circle-fill'
    }
  };

  const style = typeMap[type] || typeMap.info;

  return (
    <div
      className="agri-banner-alert shadow-sm mb-3"
      style={{
        backgroundColor: style.bg,
        borderLeftColor: style.border,
        color: style.textColor
      }}
    >
      <i className={`bi ${icon || style.defaultIcon} fs-5 flex-shrink-0 mt-1`}></i>
      <div className="flex-grow-1">
        {title && <h6 className="fw-bold mb-1" style={{ color: style.textColor }}>{title}</h6>}
        <div className="small">{message}</div>
      </div>
    </div>
  );
};

export default AlertCard;
