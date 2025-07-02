import React from 'react';
import { useNavigate } from 'react-router-dom';

const Logout: React.FC = () => {
  const navigate = useNavigate();

  React.useEffect(() => {
    // Remove currentUser from localStorage
    localStorage.removeItem('currentUser');
    alert('You have been logged out.');
    // Redirect to login page
    navigate('/');
  }, [navigate]);

  return <div>Logging out...</div>;
};

export default Logout;