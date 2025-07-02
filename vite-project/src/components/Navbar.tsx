import React from 'react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
  return (
    <nav>
      <div className="nav-left">
        <Link to="/register">Register</Link>
        <Link to="/">Login</Link>
        <Link to="/profile">Profile</Link>
        <Link to="/match">Volunteer Matching</Link>
        <Link to="/available-events">Available Events</Link>
        <Link to="/history"> Volunteer History</Link>
        <Link to="/notifications">Notifications</Link>
        <Link to="/logout">Logout</Link>
      </div>
      <div className="nav-right">
        <Link to="/admin">Admin Dashboard</Link>
      </div>
    </nav>
  );
};

export default Navbar;