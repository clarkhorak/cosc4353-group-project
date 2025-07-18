import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import apiService from '../services/api';

const states = [
  'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
  'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
  'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
  'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
];

const skillsList = ['First Aid', 'Teaching', 'Cooking', 'Driving', 'Organizing', 'Event Planning', 'Fundraising', 'Mentoring', 'Technical Support', 'Translation'];

type Availability = {
  date: string;
  time: string; 
};

const Profile: React.FC = () => {
  const { user } = useAuth();
  const [form, setForm] = useState({
    address1: '',
    city: '',
    state: '',
    zip: '',
    skills: [] as string[],
    availability: [] as Availability[],
    newDate: '',
    newTime: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [profileExists, setProfileExists] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    if (!apiService.isAuthenticated()) {
      setError('Please login first');
      return;
    }

    try {
      const profile = await apiService.getMyProfile();
      setForm({
        address1: profile.address.address1,
        city: profile.address.city,
        state: profile.address.state,
        zip: profile.address.zip_code,
        skills: profile.skills,
        availability: profile.availability,
        newDate: '',
        newTime: '',
      });
      setProfileExists(true);
    } catch (err) {
      // Profile doesn't exist yet, that's okay
      setProfileExists(false);
    }
  };

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (
      !form.address1 ||
      !form.city ||
      !form.state ||
      !form.zip ||
      form.zip.length < 5 ||
      form.skills.length === 0 ||
      form.availability.length === 0
    ) {
      alert('Please fill in all required fields properly.');
      setLoading(false);
      return;
    }

    try {
      const profileData = {
        address: {
          address1: form.address1,
          city: form.city,
          state: form.state,
          zip_code: form.zip,
        },
        skills: form.skills,
        availability: form.availability,
      };

      if (profileExists) {
        await apiService.updateProfile(profileData);
        alert('Profile updated successfully!');
      } else {
        await apiService.createProfile(profileData);
        setProfileExists(true);
        alert('Profile created successfully!');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save profile');
      alert(`Failed to save profile: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Please login to view your profile</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">User Profile</h2>
          
          <div className="mb-6 p-4 bg-blue-50 rounded-md">
            <h3 className="font-semibold text-blue-900">User Information</h3>
            <p className="text-blue-700">Email: {user.email}</p>
            <p className="text-blue-700">Name: {user.full_name}</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Address 1 *
              </label>
              <input
                type="text"
                name="address1"
                placeholder="Street address"
                maxLength={100}
                value={form.address1}
                required
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  City *
                </label>
                <input
                  type="text"
                  name="city"
                  placeholder="City"
                  maxLength={100}
                  value={form.city}
                  required
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  State *
                </label>
                <select
                  name="state"
                  value={form.state}
                  onChange={handleChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">Select State</option>
                  {states.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Zip Code *
                </label>
                <input
                  type="text"
                  name="zip"
                  placeholder="Zip Code"
                  maxLength={9}
                  minLength={5}
                  value={form.zip}
                  required
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Skills * (Select multiple with Ctrl/Cmd)
              </label>
              <select
                name="skills"
                multiple
                value={form.skills}
                onChange={handleSkillChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 min-h-[120px]"
              >
                {skillsList.map((skill) => (
                  <option key={skill} value={skill}>{skill}</option>
                ))}
              </select>
              <p className="text-sm text-gray-500 mt-1">
                Selected: {form.skills.join(', ')}
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Availability *
              </label>
              <div className="flex gap-2 mb-2">
                <input
                  type="date"
                  name="newDate"
                  value={form.newDate}
                  onChange={handleChange}
                  className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <input
                  type="time"
                  name="newTime"
                  value={form.newTime}
                  onChange={handleChange}
                  className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <button
                  type="button"
                  onClick={addAvailability}
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  + Add
                </button>
              </div>

              {form.availability.length > 0 && (
                <ul className="space-y-2">
                  {form.availability.map((a, idx) => (
                    <li key={idx} className="flex items-center justify-between p-2 bg-gray-50 rounded-md">
                      <span>{a.date} at {a.time}</span>
                      <button
                        type="button"
                        onClick={() => removeAvailability(a.date, a.time)}
                        className="text-red-600 hover:text-red-800"
                      >
                        Remove
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {error && (
              <div className="text-red-600 text-sm">
                {error}
              </div>
            )}

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {loading ? 'Saving...' : (profileExists ? 'Update Profile' : 'Create Profile')}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Profile;
