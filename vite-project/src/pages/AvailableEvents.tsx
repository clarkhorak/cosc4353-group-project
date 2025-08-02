import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import type { Event } from '../services/api';

const AvailableEvents: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const hasShownAlert = useRef(false);

  const [events, setEvents] = useState<Event[]>([]);
  const [joinedEventIds, setJoinedEventIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError('');
      try {
        if (!user && !hasShownAlert.current) {
          hasShownAlert.current = true;
          alert('Please login to view and join events.');
          navigate('/');
          return;
        }
        // Fetch events from backend
        const data = await apiService.getEvents();
        setEvents(data);
        // Fetch joined events from backend
        const history = await apiService.getHistory();
        setJoinedEventIds(history.map((h: any) => h.event_id));
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load events');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [navigate, user]);

  const handleJoin = async (event: Event) => {
    if (!user) {
      alert('You must be logged in to join events.');
      return;
    }
    try {
      await apiService.participateInEvent(event.id);
      setJoinedEventIds(prev => [...prev, event.id]);
      alert(`You joined ${event.title}`);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to join event');
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

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Please login to view events</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Available Events</h2>
          <p className="mt-2 text-gray-600">Browse and join volunteer opportunities in your area</p>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-red-800">{error}</p>
          </div>
        ) : events.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📅</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No events available</h3>
            <p className="text-gray-600">Check back later for new volunteer opportunities!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {events.map((event) => (
              <div key={event.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold text-gray-900">{event.title}</h3>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      event.status === 'open' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {event.status}
                    </span>
                  </div>
                  
                  <p className="text-gray-600 mb-4 line-clamp-3">{event.description}</p>
                  
                  <div className="space-y-2 mb-4">
                    <div className="flex items-center text-sm text-gray-500">
                      <span className="font-medium w-20">Date:</span>
                      <span>{formatDate(event.event_date)}</span>
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <span className="font-medium w-20">Time:</span>
                      <span>{formatTime(event.start_time)} - {formatTime(event.end_time)}</span>
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <span className="font-medium w-20">Location:</span>
                      <span>{event.location}</span>
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <span className="font-medium w-20">Category:</span>
                      <span className="capitalize">{event.category}</span>
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <span className="font-medium w-20">Capacity:</span>
                      <span>{event.capacity} volunteers</span>
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <span className="font-medium w-20">Urgency:</span>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        event.urgency === 'High' ? 'bg-red-100 text-red-800' :
                        event.urgency === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {event.urgency}
                      </span>
                    </div>
                    {event.required_skills && event.required_skills.length > 0 && (
                      <div className="flex items-start text-sm text-gray-500">
                        <span className="font-medium w-20">Skills:</span>
                        <div className="flex flex-wrap gap-1">
                          {event.required_skills.map((skill, index) => (
                            <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="flex justify-between items-center">
                    {joinedEventIds.includes(event.id) ? (
                      <span className="inline-flex items-center px-3 py-2 text-sm font-medium text-green-700 bg-green-100 rounded-md">
                        ✓ Joined
                      </span>
                    ) : (
                      <button
                        onClick={() => handleJoin(event)}
                        disabled={event.status !== 'open'}
                        className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        Join Event
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AvailableEvents;
