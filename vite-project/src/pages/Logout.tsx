import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';

const Logout: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const performLogout = async () => {
      try {
        await apiService.logout();
      } catch (err) {
        console.error('Logout error:', err);
      } finally {
        apiService.clearAuth();
        alert('You have been logged out.');
        navigate('/');
      }
    };

    performLogout();
  }, [navigate]);

  return <div>Logging out...</div>;
};

export default Logout;