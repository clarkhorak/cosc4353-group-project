import React, { useEffect, useState } from 'react';

type Event = {
  eventName: string;
  description: string;
  location: string;
  requiredSkills: string[];
  urgency: string;
  eventDate: string;
};

type Participation = {
  eventName: string;
  status: string;
};

type HistoryItem = Event & { status: string };

const VolunteerHistory: React.FC = () => {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const currentUserEmail = localStorage.getItem('currentUser');
  const participationKey = currentUserEmail ? `participation_${currentUserEmail}` : null;

  useEffect(() => {
    if (!participationKey) {
      setHistory([]);
      return;
    }

    const participationData = localStorage.getItem(participationKey);
    const eventsData = localStorage.getItem('events');

    if (!participationData || !eventsData) {
      setHistory([]);
      return;
    }

    const participation: Participation[] = JSON.parse(participationData);
    const events: Event[] = JSON.parse(eventsData);

    const combinedHistory: HistoryItem[] = participation.map((p) => {
      const eventInfo = events.find(e => e.eventName === p.eventName);
      return eventInfo ? { ...eventInfo, status: p.status } : null;
    }).filter(Boolean) as HistoryItem[];

    setHistory(combinedHistory);
  }, [participationKey]);

  return (
    <div>
      <h2>Volunteer History</h2>
      {history.length === 0 ? (
        <p>No participation history yet.</p>
      ) : (
        history.map((item, idx) => (
          <div key={idx} style={{
            border: '1px solid #ccc',
            borderRadius: '8px',
            padding: '15px',
            marginBottom: '15px',
            maxWidth: '600px',
            backgroundColor: '#fafafa'
          }}>
            <h3 style={{ marginBottom: '10px' }}>{item.eventName}</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '150px 1fr', rowGap: '8px', columnGap: '10px' }}>
              <strong>Description:</strong>
              <span>{item.description || 'N/A'}</span>

              <strong>Location:</strong>
              <span>{item.location || 'N/A'}</span>

              <strong>Required Skills:</strong>
              <span>{item.requiredSkills.length > 0 ? item.requiredSkills.join(', ') : 'N/A'}</span>

              <strong>Urgency:</strong>
              <span>{item.urgency || 'N/A'}</span>

              <strong>Event Date:</strong>
              <span>{item.eventDate || 'N/A'}</span>

              <strong>Status:</strong>
              <span>{item.status}</span>
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default VolunteerHistory;