import React from 'react';

const LoadingSpinner = ({ text = 'Analyzing agricultural telemetry...' }) => {
  return (
    <div className="d-flex flex-column align-items-center justify-content-center p-5 text-center">
      <div className="spinner-agri mb-3"></div>
      <p className="text-muted fw-semibold mb-0 small">{text}</p>
    </div>
  );
};

export default LoadingSpinner;
