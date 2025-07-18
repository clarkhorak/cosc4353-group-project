import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

type Event = {
  eventName: string;
  description: string;
  location: string;
  requiredSkills: string[];
  urgency: string;
  eventDate: string;   
  eventTime: string;   
};

type Participation = {
  eventName: string;
  description: string;
  location: string;
  requiredSkills: string[];
  urgency: string;
  eventDate: string;
  eventTime: string;
  status: string;
};

const AvailableEvents: React.FC = () => {
  const navigate = useNavigate();
  const currentUserEmail = localStorage.getItem('currentUser');
  const participationKey = currentUserEmail ? `participation_${currentUserEmail}` : null;
  const hasShownAlert = useRef(false);

  const [events, setEvents] = useState<Event[]>([]);
  const [joinedEvents, setJoinedEvents] = useState<string[]>([]);

  useEffect(() => {
    if (!currentUserEmail && !hasShownAlert.current) {
      hasShownAlert.current = true;
      alert('Please login to view and join events.');
      navigate('/');
      return;
    }

    const savedEvents = localStorage.getItem('events');
    if (savedEvents) setEvents(JSON.parse(savedEvents));

    if (participationKey) {
      const savedParticipation = localStorage.getItem(participationKey);
      if (savedParticipation) {
        const participation: Participation[] = JSON.parse(savedParticipation);
        const joined = participation.map(p => p.eventName);
        setJoinedEvents(joined);
      } else {
        setJoinedEvents([]);
      }
    }
  }, [currentUserEmail, participationKey, navigate]);

  const updateLocalStorage = (updatedParticipation: Participation[]) => {
    if (!participationKey) return;
    localStorage.setItem(participationKey, JSON.stringify(updatedParticipation));
  };

  const handleJoin = (event: Event) => {
    if (!participationKey) {
      alert('You must be logged in to join events.');
      return;
    }

    const participation: Participation[] = JSON.parse(localStorage.getItem(participationKey) || '[]');

    if (participation.find(p => p.eventName === event.eventName)) {
      alert('You already joined this event.');
      return;
    }

    const newEntry: Participation = {
      eventName: event.eventName,
      description: event.description,
      location: event.location,
      requiredSkills: event.requiredSkills,
      urgency: event.urgency,
      eventDate: event.eventDate,
      eventTime: event.eventTime,
      status: 'Pending',
    };

    const updated = [...participation, newEntry];
    updateLocalStorage(updated);
    setJoinedEvents(prev => [...prev, event.eventName]);
    alert(`You joined ${event.eventName}`);
  };

  const handleUnjoin = (event: Event) => {
    if (!participationKey) {
      alert('You must be logged in to unjoin events.');
      return;
    }

    const participation: Participation[] = JSON.parse(localStorage.getItem(participationKey) || '[]');
    const updated = participation.filter(p => p.eventName !== event.eventName);

    updateLocalStorage(updated);
    setJoinedEvents(prev => prev.filter(name => name !== event.eventName));
    alert(`You unjoined ${event.eventName}`);
  };

  return (
    <div>
      <h2>Available Events</h2>
      {events.length === 0 ? (
        <p>No events available right now.</p>
      ) : (
        events.map((e, idx) => (
          <div key={idx} style={{ border: '1px solid gray', padding: '10px', marginBottom: '10px' }}>
            <h3>{e.eventName}</h3>
            <p>{e.description}</p>
            <p><strong>Date:</strong> {e.eventDate} at {e.eventTime}</p>
            <p><strong>Location:</strong> {e.location}</p>
            <p><strong>Urgency:</strong> {e.urgency}</p>
            <p><strong>Skills Needed:</strong> {e.requiredSkills.join(', ')}</p>
            {joinedEvents.includes(e.eventName) ? (
              <button onClick={() => handleUnjoin(e)}>Unjoin</button>
            ) : (
              <button onClick={() => handleJoin(e)}>Join</button>
            )}
          </div>
        ))
      )}
    </div>
  );
};

export default AvailableEvents;
