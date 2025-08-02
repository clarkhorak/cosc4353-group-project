const API_BASE_URL = 'http://localhost:8000';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  full_name: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  created_at: string;
  is_active: boolean;
}

export interface ProfileCreate {
  address: {
    address1: string;
    city: string;
    state: string;
    zip_code: string;
  };
  skills: string[];
  availability: {
    date: string;
    time: string;
  }[];
  preferences?: string;
}

export interface ProfileUpdate {
  address?: {
    address1: string;
    city: string;
    state: string;
    zip_code: string;
  };
  skills?: string[];
  availability?: {
    date: string;
    time: string;
  }[];
  preferences?: string;
}

export interface Profile {
  user_id: string;
  address: {
    address1: string;
    city: string;
    state: string;
    zip_code: string;
  };
  skills: string[];
  availability: {
    date: string;
    time: string;
  }[];
  preferences?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Event {
  id: number;
  title: string;
  description?: string;
  category: string;
  event_date: string;
  start_time: string;
  end_time: string;
  location: string;
  capacity: number;
  requirements?: string;
  required_skills?: string[];
  urgency: string;
  status: string;
  created_at: string;
  updated_at?: string;
}

export interface EventCreate {
  title: string;
  description?: string;
  category: string;
  event_date: string;
  start_time: string;
  end_time: string;
  location: string;
  capacity: number;
  requirements?: string;
  required_skills?: string[];
  urgency?: string;
  status?: string;
}

export interface VolunteerHistory {
  id: number;
  volunteer_id: string;
  event_id: number;
  event_name: string;
  event_date: string;
  event_time: string;
  location: string;
  status: string;
  skills_used?: string[];
  rating?: number;
  joined_at: string;
  updated_at?: string;
}

export interface VolunteerStats {
  volunteer_id: string;
  total_events: number;
  completed_events: number;
  pending_events: number;
  cancelled_events: number;
  no_show_events: number;
  completion_rate: number;
}

export interface Notification {
  id: number;
  user_id: string;
  type: string;
  title: string;
  message: string;
  event_id?: string;
  created_at: string;
  is_read: boolean;
}

export interface NotificationCreate {
  type: string;
  title: string;
  message: string;
  event_id?: string;
}

class ApiService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('access_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      let errorMessage = `HTTP error! status: ${response.status}`;
      
      try {
        const errorData = await response.json();
        
        // Handle different FastAPI error response formats
        if (errorData.detail) {
          if (Array.isArray(errorData.detail)) {
            // Validation errors
            const validationErrors = errorData.detail.map((err: any) => 
              `${err.loc?.join('.') || 'field'}: ${err.msg}`
            ).join(', ');
            errorMessage = `Validation error: ${validationErrors}`;
          } else {
            // Single error message
            errorMessage = errorData.detail;
          }
        } else if (errorData.message) {
          errorMessage = errorData.message;
        } else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      } catch (parseError) {
        // If we can't parse the error response, use the status text
        errorMessage = response.statusText || `HTTP error! status: ${response.status}`;
      }
      
      throw new Error(errorMessage);
    }
    return response.json();
  }

  // Authentication endpoints
  async register(data: RegisterRequest): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return this.handleResponse<User>(response);
  }

  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return this.handleResponse<AuthResponse>(response);
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<User>(response);
  }

  async logout(): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/auth/logout`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
    });
    if (response.ok) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('currentUser');
    }
  }

  // Profile endpoints
  async createProfile(data: ProfileCreate): Promise<Profile> {
    const response = await fetch(`${API_BASE_URL}/profiles/`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });
    return this.handleResponse<Profile>(response);
  }

  async getMyProfile(): Promise<Profile> {
    const response = await fetch(`${API_BASE_URL}/profiles/me`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<Profile>(response);
  }

  async updateProfile(data: ProfileUpdate): Promise<Profile> {
    const response = await fetch(`${API_BASE_URL}/profiles/me`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });
    return this.handleResponse<Profile>(response);
  }

  async deleteProfile(): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/profiles/me`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Failed to delete profile');
    }
  }

  async getAllProfiles(): Promise<Profile[]> {
    const response = await fetch(`${API_BASE_URL}/profiles/`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<Profile[]>(response);
  }

  async searchProfilesBySkills(skills: string[]): Promise<Profile[]> {
    const params = new URLSearchParams();
    skills.forEach(skill => params.append('skills', skill));
    const response = await fetch(`${API_BASE_URL}/profiles/search/skills?${params}`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<Profile[]>(response);
  }

  async searchProfilesByLocation(city: string, state?: string): Promise<Profile[]> {
    const params = new URLSearchParams({ city });
    if (state) params.append('state', state);
    const response = await fetch(`${API_BASE_URL}/profiles/search/location?${params}`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<Profile[]>(response);
  }

  // Event endpoints
  async getEvents(search?: string, category?: string, status?: string): Promise<Event[]> {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (category) params.append('category', category);
    if (status) params.append('status', status);
    
    const response = await fetch(`${API_BASE_URL}/events/?${params}`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<Event[]>(response);
  }

  async getEvent(eventId: number): Promise<Event> {
    const response = await fetch(`${API_BASE_URL}/events/${eventId}`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<Event>(response);
  }

  async createEvent(data: EventCreate): Promise<Event> {
    const response = await fetch(`${API_BASE_URL}/events/`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });
    return this.handleResponse<Event>(response);
  }

  async updateEvent(eventId: number, data: Partial<EventCreate>): Promise<Event> {
    const response = await fetch(`${API_BASE_URL}/events/${eventId}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });
    return this.handleResponse<Event>(response);
  }

  async deleteEvent(eventId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/events/${eventId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Failed to delete event');
    }
  }

  // History endpoints
  async getHistory(): Promise<VolunteerHistory[]> {
    const response = await fetch(`${API_BASE_URL}/history/`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<VolunteerHistory[]>(response);
  }

  async getStats(): Promise<VolunteerStats> {
    const response = await fetch(`${API_BASE_URL}/history/stats`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<VolunteerStats>(response);
  }

  async participateInEvent(eventId: number, skills?: string[]): Promise<VolunteerHistory> {
    const response = await fetch(`${API_BASE_URL}/history/participate/${eventId}`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ skills }),
    });
    return this.handleResponse<VolunteerHistory>(response);
  }

  async updateParticipationStatus(eventId: number, status: string, rating?: number): Promise<VolunteerHistory> {
    const response = await fetch(`${API_BASE_URL}/history/${eventId}/status`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ status, rating }),
    });
    return this.handleResponse<VolunteerHistory>(response);
  }

  // Notification endpoints
  async getNotifications(): Promise<Notification[]> {
    const response = await fetch(`${API_BASE_URL}/notifications/`, {
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<Notification[]>(response);
  }

  async createNotification(data: NotificationCreate): Promise<Notification> {
    const response = await fetch(`${API_BASE_URL}/notifications/`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });
    return this.handleResponse<Notification>(response);
  }

  async markNotificationAsRead(notificationId: number): Promise<Notification> {
    const response = await fetch(`${API_BASE_URL}/notifications/${notificationId}/read`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
    });
    return this.handleResponse<Notification>(response);
  }

  async deleteNotification(notificationId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/notifications/${notificationId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Failed to delete notification');
    }
  }

  // Utility methods
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  setToken(token: string): void {
    localStorage.setItem('access_token', token);
  }

  clearAuth(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('currentUser');
  }
}

export const apiService = new ApiService(); 