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
};

const Notifications: React.FC = () => {
  const [notifications, setNotifications] = useState<string[]>([]);

  useEffect(() => {
    const currentUserEmail = localStorage.getItem('currentUser');
    const profileData = currentUserEmail ? localStorage.getItem(`profile_${currentUserEmail}`) : null;
    const eventData = localStorage.getItem('events');
    if (!profileData || !eventData) return;

    const volunteer: Volunteer = JSON.parse(profileData);
    const events: Event[] = JSON.parse(eventData);
    const today = new Date();

    const newNotifications: string[] = [];

    const formatTime = (timeStr?: string) => {
      if (!timeStr || !timeStr.includes(':')) return 'Time not set';
      const [hour, minute] = timeStr.split(':');
      const hourNum = parseInt(hour, 10);
      const ampm = hourNum >= 12 ? 'PM' : 'AM';
      const formattedHour = hourNum % 12 === 0 ? 12 : hourNum % 12;
      return `${formattedHour}:${minute} ${ampm}`;
    };

    events.forEach((event) => {
      const eventDateTime = new Date(`${event.eventDate}T${event.eventTime}`);
      const isMatched = event.requiredSkills.some(skill =>
        volunteer.skills.includes(skill)
      );

      const formattedDate = event.eventDate;
      const formattedTime = formatTime(event.eventTime);

      if (isMatched) {
        newNotifications.push(
          `You have been assigned to "${event.eventName}" on ${formattedDate} at ${formattedTime}.`
        );

        const diffInDays = Math.floor(
          (eventDateTime.getTime() - today.getTime()) / (1000 * 60 * 60 * 24)
        );
        if (diffInDays === 1) {
          newNotifications.push(
            `Reminder: "${event.eventName}" is tomorrow at ${formattedTime}.`
          );
        }
      } else {
        newNotifications.push(
          `New event available: "${event.eventName}" on ${formattedDate} at ${formattedTime}.`
        );
      }
    });

    setNotifications(newNotifications);
  }, []);

  return (
    <div>
      <h2>Notifications</h2>
      {notifications.length === 0 ? (
        <p>No notifications at this time.</p>
      ) : (
        <ul>
          {notifications.map((note, idx) => (
            <li key={idx}>{note}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Notifications;