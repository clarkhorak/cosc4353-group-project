import React, { useState, useEffect } from 'react';

const states = [
  'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
  'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
  'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
  'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
];

const skillsList = ['First Aid', 'Teaching', 'Cooking', 'Driving', 'Organizing'];

type Availability = {
  date: string;
  time: string; 
};

const Profile: React.FC = () => {
  const [form, setForm] = useState({
    email: '',
    fullName: '',
    address1: '',
    address2: '',
    city: '',
    state: '',
    zip: '',
    skills: [] as string[],
    preferences: '',
    availability: [] as Availability[],
    newDate: '',
    newTime: '',
  });

  const currentUserEmail = localStorage.getItem('currentUser');

  useEffect(() => {
    if (!currentUserEmail) return;

    const savedProfile = localStorage.getItem(`profile_${currentUserEmail}`);
    if (savedProfile) {
      setForm(JSON.parse(savedProfile));
    } else {
      setForm(f => ({ ...f, email: currentUserEmail }));
    }
  }, [currentUserEmail]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSkillChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selected = Array.from(e.target.selectedOptions, (opt) => opt.value);
    setForm({ ...form, skills: selected });
  };

  const addAvailability = () => {
    if (form.newDate && form.newTime) {
      const exists = form.availability.some(
        (a) => a.date === form.newDate && a.time === form.newTime
      );
      if (!exists) {
        setForm({
          ...form,
          availability: [...form.availability, { date: form.newDate, time: form.newTime }],
          newDate: '',
          newTime: ''
        });
      }
    }
  };

  const removeAvailability = (date: string, time: string) => {
    setForm({
      ...form,
      availability: form.availability.filter(a => !(a.date === date && a.time === time))
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (
      !form.email ||
      !form.fullName ||
      !form.address1 ||
      !form.city ||
      !form.state ||
      !form.zip ||
      form.zip.length < 5 ||
      form.skills.length === 0 ||
      form.availability.length === 0
    ) {
      alert('Please fill in all required fields properly.');
      return;
    }

    if (!currentUserEmail || currentUserEmail !== form.email) {
      alert('Email does not match logged-in user!');
      return;
    }

    localStorage.setItem(`profile_${currentUserEmail}`, JSON.stringify(form));
    alert('Profile saved successfully!');
  };

  return (
    <div>
      <h2>User Profile</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" name="email" placeholder="Email (used as login)" maxLength={100}
          value={form.email} readOnly required onChange={handleChange} /><br />

        <input name="fullName" placeholder="Full Name" maxLength={50}
          value={form.fullName} required onChange={handleChange} /><br />

        <input name="address1" placeholder="Address 1" maxLength={100}
          value={form.address1} required onChange={handleChange} /><br />

        <input name="address2" placeholder="Address 2 (Optional)" maxLength={100}
          value={form.address2} onChange={handleChange} /><br />

        <input name="city" placeholder="City" maxLength={100}
          value={form.city} required onChange={handleChange} /><br />

        <select name="state" value={form.state} onChange={handleChange} required>
          <option value="">Select State</option>
          {states.map((s) => <option key={s} value={s}>{s}</option>)}
        </select><br />

        <input name="zip" placeholder="Zip Code" maxLength={9} minLength={5}
          value={form.zip} required onChange={handleChange} /><br />

        <label>Skills (Select multiple with Ctrl/Cmd):</label><br />
        <select name="skills" multiple value={form.skills} onChange={handleSkillChange} required>
          {skillsList.map((skill) => <option key={skill} value={skill}>{skill}</option>)}
        </select><br />

        <textarea name="preferences" placeholder="Preferences (Optional)"
          value={form.preferences} onChange={handleChange} /><br />

        <label>Availability:</label><br />
        <input type="date" name="newDate" value={form.newDate} onChange={handleChange} />
        <input type="time" name="newTime" value={form.newTime} onChange={handleChange} />
        <button type="button" onClick={addAvailability}>+ Add</button>

        <ul>
          {form.availability.map((a, idx) => (
            <li key={idx}>
              {a.date} at {a.time}{' '}
              <button type="button" onClick={() => removeAvailability(a.date, a.time)}>Remove</button>
            </li>
          ))}
        </ul>

        <br />
        <button type="submit">Save Profile</button>
      </form>
    </div>
  );
};

export default Profile;
