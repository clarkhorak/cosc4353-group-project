import React, { useState, useEffect } from 'react';
import apiService from '../services/api';

type Event = {
  id?: number;
  title: string;
  description: string;
  location: string;
  requirements: string;
  category: string;
  event_date: string;
  start_time: string;
  end_time: string;
  capacity: number;
  status: string;
};

const skillsList = ['First Aid', 'Teaching', 'Cooking', 'Driving', 'Organizing'];
const urgencies = ['Low', 'Medium', 'High'];
const ADMIN_PASSWORD = 'admin123';

const AdminDashboard: React.FC = () => {
  const [authenticated, setAuthenticated] = useState(false);
  const [form, setForm] = useState({
    title: '',
    description: '',
    location: '',
    requirements: '',
    category: '',
    event_date: '',
    start_time: '',
    end_time: '',
    capacity: 1,
    status: 'open',
  });
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const password = prompt('Enter admin password:');
    if (password === ADMIN_PASSWORD) {
      setAuthenticated(true);
      fetchEvents();
    } else {
      alert('Access denied.');
      window.location.href = '/';
    }
    // eslint-disable-next-line
  }, []);

  const fetchEvents = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await apiService.getEvents();
      setEvents(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load events');
    } finally {
      setLoading(false);
    }
  };

  if (!authenticated) return null;

  const handleChange = (e: React.ChangeEvent<any>) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (
      !form.title || !form.description || !form.location ||
      !form.category || !form.event_date || !form.start_time || !form.end_time || !form.capacity
    ) {
      alert('Please fill in all required fields.');
      return;
    }
    try {
      await apiService.createEvent(form);
      alert('Event created successfully!');
      setForm({
        title: '',
        description: '',
        location: '',
        requirements: '',
        category: '',
        event_date: '',
        start_time: '',
        end_time: '',
        capacity: 1,
        status: 'open',
      });
      fetchEvents();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create event');
    }
  };

  const formatTime = (timeStr?: string) => {
    if (!timeStr || !timeStr.includes(':')) return 'Time not set';
    const [hour, minute] = timeStr.split(':');
    const hourNum = parseInt(hour, 10);
    const ampm = hourNum >= 12 ? 'PM' : 'AM';
    const formattedHour = hourNum % 12 === 0 ? 12 : hourNum % 12;
    return `${formattedHour}:${minute} ${ampm}`;
  };

  return (
    <div>
      <h2>Admin Dashboard - Create Event</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="title" placeholder="Event Title" value={form.title} onChange={handleChange} required /><br />
        <textarea name="description" placeholder="Event Description" value={form.description} onChange={handleChange} required /><br />
        <textarea name="location" placeholder="Event Location" value={form.location} onChange={handleChange} required /><br />
        <input type="text" name="category" placeholder="Category" value={form.category} onChange={handleChange} required /><br />
        <input type="text" name="requirements" placeholder="Requirements (comma separated)" value={form.requirements} onChange={handleChange} /><br />
        <input type="number" name="capacity" placeholder="Capacity" value={form.capacity} min={1} onChange={handleChange} required /><br />
        <label>Status:</label><br />
        <select name="status" value={form.status} onChange={handleChange} required>
          <option value="open">Open</option>
          <option value="closed">Closed</option>
          <option value="cancelled">Cancelled</option>
        </select><br />
        <label>Event Date:</label><br />
        <input type="date" name="event_date" value={form.event_date} onChange={handleChange} required /><br />
        <label>Start Time:</label><br />
        <input type="time" name="start_time" value={form.start_time} onChange={handleChange} required /><br />
        <label>End Time:</label><br />
        <input type="time" name="end_time" value={form.end_time} onChange={handleChange} required /><br />
        <button type="submit">Create Event</button>
      </form>
      <h3>Created Events</h3>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : events.length === 0 ? (
        <p>No events created yet.</p>
      ) : (
        <ul>
          {events.map((e, idx) => (
            <li key={e.id || idx}>
              <strong>{e.title}</strong> — {e.event_date} {e.start_time && `at ${formatTime(e.start_time)}`} ({e.status})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AdminDashboard;
