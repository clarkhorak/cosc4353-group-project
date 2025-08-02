import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';

type Event = {
  id?: number;
  title: string;
  description?: string;
  location: string;
  requirements?: string;
  category: string;
  event_date: string;
  start_time: string;
  end_time: string;
  capacity: number;
  status: string;
};

type User = {
  id: string;
  email: string;
  full_name: string;
  role: string;
  created_at: string;
  is_active: boolean;
};

const skillsList = ['First Aid', 'Teaching', 'Cooking', 'Driving', 'Organizing'];
const urgencies = ['Low', 'Medium', 'High'];

const AdminDashboard: React.FC = () => {
  const { isAdmin, isAuthenticated, user: currentUser } = useAuth();
  const navigate = useNavigate();
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
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState<'events' | 'users'>('events');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/');
      return;
    }

    if (!isAdmin()) {
      alert('Access denied. Admin privileges required.');
      navigate('/');
      return;
    }

    fetchData();
  }, [isAuthenticated, isAdmin, navigate]);

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      console.log('Fetching data for admin dashboard...');
      
      // Fetch events and users separately to better debug issues
      try {
        const eventsData = await apiService.getEvents();
        console.log('Events data:', eventsData);
        setEvents(eventsData);
      } catch (eventsError) {
        console.error('Error fetching events:', eventsError);
        setEvents([]);
      }
      
      try {
        const usersData = await apiService.getUsers();
        console.log('Users data:', usersData);
        setUsers(usersData);
      } catch (usersError) {
        console.error('Error fetching users:', usersError);
        setError(`Failed to load users: ${usersError instanceof Error ? usersError.message : 'Unknown error'}`);
        setUsers([]);
      }
      
    } catch (err) {
      console.error('Error fetching data:', err);
      setError(err instanceof Error ? err.message : 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated || !isAdmin()) {
    return null;
  }

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
      fetchData();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to create event');
    }
  };

  const handlePromoteUser = async (email: string) => {
    try {
      await apiService.promoteUser(email);
      alert('User promoted to admin successfully!');
      fetchData();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to promote user');
    }
  };

  const handleDemoteUser = async (email: string) => {
    try {
      await apiService.demoteUser(email);
      alert('User demoted to volunteer successfully!');
      fetchData();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to demote user');
    }
  };

  const handleDeleteUser = async (email: string, fullName: string) => {
    const confirmed = window.confirm(
      `Are you sure you want to delete user "${fullName}" (${email})?\n\nThis action cannot be undone.`
    );
    
    if (!confirmed) {
      return;
    }
    
    try {
      await apiService.deleteUser(email);
      alert('User deleted successfully!');
      fetchData();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete user');
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
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Admin Dashboard</h1>
      
      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('events')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'events'
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Event Management
          </button>
          <button
            onClick={() => setActiveTab('users')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'users'
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            User Management
          </button>
        </nav>
      </div>

      {activeTab === 'events' && (
        <div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">Create New Event</h2>
          <form onSubmit={handleSubmit} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">Event Title</label>
                <input
                  type="text"
                  name="title"
                  value={form.title}
                  onChange={handleChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">Category</label>
                <input
                  type="text"
                  name="category"
                  value={form.category}
                  onChange={handleChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  required
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-gray-700 text-sm font-bold mb-2">Description</label>
                <textarea
                  name="description"
                  value={form.description}
                  onChange={handleChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  rows={3}
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">Location</label>
                <input
                  type="text"
                  name="location"
                  value={form.location}
                  onChange={handleChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">Requirements</label>
                <input
                  type="text"
                  name="requirements"
                  value={form.requirements}
                  onChange={handleChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  placeholder="Comma separated"
                />
              </div>
              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">Capacity</label>
                <input
                  type="number"
                  name="capacity"
                  value={form.capacity}
                  onChange={handleChange}
                  min={1}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">Status</label>
                <select
                  name="status"
                  value={form.status}
                  onChange={handleChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  required
                >
                  <option value="open">Open</option>
                  <option value="closed">Closed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>
              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">Event Date</label>
                <input
                  type="date"
                  name="event_date"
                  value={form.event_date}
                  onChange={handleChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">Start Time</label>
                <input
                  type="time"
                  name="start_time"
                  value={form.start_time}
                  onChange={handleChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 text-sm font-bold mb-2">End Time</label>
                <input
                  type="time"
                  name="end_time"
                  value={form.end_time}
                  onChange={handleChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  required
                />
              </div>
            </div>
            <div className="flex items-center justify-end mt-6">
              <button
                type="submit"
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              >
                Create Event
              </button>
            </div>
          </form>

          <h3 className="text-xl font-semibold text-gray-900 mb-4">Created Events</h3>
          {loading ? (
            <p>Loading...</p>
          ) : error ? (
            <p className="text-red-600">{error}</p>
          ) : events.length === 0 ? (
            <p>No events created yet.</p>
          ) : (
            <div className="bg-white shadow overflow-hidden sm:rounded-md">
              <ul className="divide-y divide-gray-200">
                {events.map((event, idx) => (
                  <li key={event.id || idx} className="px-6 py-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-lg font-medium text-gray-900">{event.title}</h4>
                        <p className="text-sm text-gray-500">
                          {event.event_date} at {formatTime(event.start_time)} - {event.status}
                        </p>
                        <p className="text-sm text-gray-500">{event.location}</p>
                      </div>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        event.status === 'open' ? 'bg-green-100 text-green-800' :
                        event.status === 'closed' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {event.status}
                      </span>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {activeTab === 'users' && (
        <div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">User Management</h2>
          {loading ? (
            <p>Loading...</p>
          ) : error ? (
            <p className="text-red-600">{error}</p>
          ) : users.length === 0 ? (
            <p>No users found.</p>
          ) : (
            <div className="bg-white shadow overflow-hidden sm:rounded-md">
              <ul className="divide-y divide-gray-200">
                {users.map((user) => (
                  <li key={user.id} className="px-6 py-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-lg font-medium text-gray-900">{user.full_name}</h4>
                        <p className="text-sm text-gray-500">{user.email}</p>
                        <p className="text-sm text-gray-500">Joined: {new Date(user.created_at).toLocaleDateString()}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                          user.role === 'admin' ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'
                        }`}>
                          {user.role}
                        </span>
                        {user.email === currentUser?.email && (
                          <span className="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">
                            You
                          </span>
                        )}
                        {user.role === 'volunteer' ? (
                          <button
                            onClick={() => handlePromoteUser(user.email)}
                            className="bg-green-600 hover:bg-green-700 text-white text-xs px-3 py-1 rounded"
                          >
                            Promote to Admin
                          </button>
                        ) : (
                          <button
                            onClick={() => handleDemoteUser(user.email)}
                            className="bg-yellow-600 hover:bg-yellow-700 text-white text-xs px-3 py-1 rounded"
                          >
                            Demote to Volunteer
                          </button>
                        )}
                        {user.email !== currentUser?.email && (
                          <button
                            onClick={() => handleDeleteUser(user.email, user.full_name)}
                            className="bg-red-600 hover:bg-red-700 text-white text-xs px-3 py-1 rounded"
                          >
                            Delete User
                          </button>
                        )}
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
