import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Register: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !password) {
      alert('Email and password are required.');
      return;
    }

    const users = JSON.parse(localStorage.getItem('users') || '{}');

    if (users[email]) {
      alert('This email is already registered.');
      return;
    }

    users[email] = { password };
    localStorage.setItem('users', JSON.stringify(users));

    alert('Registration successful!');
    navigate('/');
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          required
          onChange={(e) => setEmail(e.target.value)}
        /><br />
        <input
          type="password"
          placeholder="Password"
          value={password}
          required
          onChange={(e) => setPassword(e.target.value)}
        /><br />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
