import React, { useState, useEffect } from 'react';

type Event = {
  eventName: string;
  description: string;
  location: string;
  requiredSkills: string[];
  urgency: string;
  eventDate: string;
  eventTime: string;
};

const skillsList = ['First Aid', 'Teaching', 'Cooking', 'Driving', 'Organizing'];
const urgencies = ['Low', 'Medium', 'High'];
const ADMIN_PASSWORD = 'admin123';

const AdminDashboard: React.FC = () => {
  const [authenticated, setAuthenticated] = useState(false);
  const [form, setForm] = useState<Event>({
    eventName: '',
    description: '',
    location: '',
    requiredSkills: [],
    urgency: '',
    eventDate: '',
    eventTime: '',
  });

  const [events, setEvents] = useState<Event[]>(() => {
    const saved = localStorage.getItem('events');
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    const password = prompt('Enter admin password:');
    if (password === ADMIN_PASSWORD) {
      setAuthenticated(true);
    } else {
      alert('Access denied.');
      window.location.href = '/';
    }
  }, []);

  if (!authenticated) return null;

  const handleChange = (e: React.ChangeEvent<any>) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSkillsChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = Array.from(e.target.selectedOptions, opt => opt.value);
    setForm({ ...form, requiredSkills: selected });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (
      !form.eventName || !form.description || !form.location ||
      form.requiredSkills.length === 0 || !form.urgency ||
      !form.eventDate || !form.eventTime
    ) {
      alert('Please fill in all required fields.');
      return;
    }

    const newEvent = { ...form };
    const updatedEvents = [...events, newEvent];
    setEvents(updatedEvents);
    localStorage.setItem('events', JSON.stringify(updatedEvents));
    alert('Event created successfully!');

    setForm({
      eventName: '',
      description: '',
      location: '',
      requiredSkills: [],
      urgency: '',
      eventDate: '',
      eventTime: '',
    });
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
        <input type="text" name="eventName" placeholder="Event Name" value={form.eventName} onChange={handleChange} required /><br />
        <textarea name="description" placeholder="Event Description" value={form.description} onChange={handleChange} required /><br />
        <textarea name="location" placeholder="Event Location" value={form.location} onChange={handleChange} required /><br />

        <label>Required Skills:</label><br />
        <select name="requiredSkills" multiple value={form.requiredSkills} onChange={handleSkillsChange} required>
          {skillsList.map(skill => <option key={skill} value={skill}>{skill}</option>)}
        </select><br />

        <label>Urgency:</label><br />
        <select name="urgency" value={form.urgency} onChange={handleChange} required>
          <option value="">Select Urgency</option>
          {urgencies.map(u => <option key={u} value={u}>{u}</option>)}
        </select><br />

        <label>Event Date:</label><br />
        <input type="date" name="eventDate" value={form.eventDate} onChange={handleChange} required /><br />

        <label>Event Time:</label><br />
        <input type="time" name="eventTime" value={form.eventTime} onChange={handleChange} required /><br />

        <button type="submit">Create Event</button>
      </form>

      <h3>Created Events</h3>
      {events.length === 0 ? (
        <p>No events created yet.</p>
      ) : (
        <ul>
          {events.map((e, idx) => (
            <li key={idx}>
              <strong>{e.eventName}</strong> — {e.eventDate} at {formatTime(e.eventTime)} ({e.urgency})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AdminDashboard;