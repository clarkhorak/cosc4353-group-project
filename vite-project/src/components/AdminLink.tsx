import React from 'react';
import { Link } from 'react-router-dom';

const AdminLink: React.FC = () => {
  return (
    <div style={{ textAlign: 'right', padding: '10px', borderTop: '1px solid #ccc' }}>
      <Link to="/admin" style={{ fontWeight: 'bold' }}>
        Admin Dashboard
      </Link>
    </div>
  );
};

export default AdminLink;