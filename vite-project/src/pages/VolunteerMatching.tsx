import React, { useEffect, useState } from 'react';

type Event = {
  eventName: string;
  description: string;
  location: string;
  requiredSkills: string[];
  urgency: string;
  eventDate: string;
  eventTime: string;
};

type Volunteer = {
  fullName: string;
  skills: string[];
  availability: { date: string; time: string }[];
};

type Match = {
  volunteerName: string;
  matchedEvent: string;
};

const VolunteerMatching: React.FC = () => {
  const [matches, setMatches] = useState<Match[]>([]);

  useEffect(() => {
    const currentUserEmail = localStorage.getItem('currentUser');
    const profileData = currentUserEmail ? localStorage.getItem(`profile_${currentUserEmail}`) : null;
    const eventData = localStorage.getItem('events');

    if (!profileData || !eventData) return;

    const volunteer: Volunteer = JSON.parse(profileData);
    const events: Event[] = JSON.parse(eventData);

    const matchedEvents = events.filter(event => {
      const skillMatch = event.requiredSkills.some(skill => volunteer.skills.includes(skill));
      const timeMatch = volunteer.availability.some(avail =>
        avail.date === event.eventDate && avail.time === event.eventTime
      );
      return skillMatch && timeMatch;
    });

    const formattedMatches = matchedEvents.map(event => ({
      volunteerName: volunteer.fullName,
      matchedEvent: `${event.eventName} – ${event.eventDate} at ${event.eventTime}`,
    }));

    setMatches(formattedMatches);
  }, []);

  return (
    <div>
      <h2>Volunteer Matching</h2>
      {matches.length === 0 ? (
        <p>No matching events found. Make sure your profile includes skills and availability that match existing events.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Volunteer Name</th>
              <th>Matched Event</th>
            </tr>
          </thead>
          <tbody>
            {matches.map((m, idx) => (
              <tr key={idx}>
                <td>{m.volunteerName}</td>
                <td>{m.matchedEvent}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default VolunteerMatching;
