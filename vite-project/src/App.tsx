import React from 'react';

import './index.css';
import './App.css';

import { Routes, Route } from 'react-router-dom';

import Navbar from './components/Navbar'; 
import AdminLink from './components/AdminLink'; 

import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile.tsx';
import AdminDashboard from './pages/AdminDashboard';
import VolunteerMatching from './pages/VolunteerMatching';
import VolunteerHistory from './pages/VolunteerHistory';
import Notifications from './pages/Notifications';
import AvailableEvents from './pages/AvailableEvents';
import Logout from './pages/Logout';

const App: React.FC = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/match" element={<VolunteerMatching />} />
        <Route path="/history" element={<VolunteerHistory />} />
        <Route path="/notifications" element={<Notifications />} />
        <Route path="/available-events" element={<AvailableEvents />} />
        <Route path="/logout" element={<Logout />} />
      </Routes>
    </>
  );
};

export default App;