import React from 'react';

const Notification = ({ message, type }) => {
  if (!message) return null;

  const styles = {
    position: 'fixed',
    top: '20px',
    left: '50%',
    transform: 'translateX(-50%)',
    padding: '12px 24px',
    borderRadius: '4px',
    backgroundColor: type === 'success' ? '#4CAF50' : '#f44336',
    color: 'white',
    boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
    zIndex: 1000,
    animation: 'fadeIn 0.3s ease-in-out'
  };

  return (
    <div style={styles}>
      {message}
    </div>
  );
};

export default Notification; 