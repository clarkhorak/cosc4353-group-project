# Volunteer Management System

A full-stack web application for managing volunteer opportunities, built with React (Frontend) and FastAPI (Backend).

## 🚀 Project Overview

This system allows organizations to post volunteer events and volunteers to find opportunities that match their skills and availability. The application includes user authentication, profile management, event management, volunteer matching, and comprehensive notification systems.

## 📁 Project Structure

```
cosc4353-group-project/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints (auth, profile, events, history, matching, notifications)
│   │   ├── models/         # Pydantic data models
│   │   ├── services/       # Business logic services
│   │   └── utils/          # Utilities and exceptions
│   ├── requirements.txt    # Python dependencies
│   ├── test_*.py          # Unit tests
│   └── test_api_endpoints.py # Comprehensive API tests
├── vite-project/           # React frontend
│   ├── src/
│   │   ├── components/     # React components (Navbar, etc.)
│   │   ├── pages/          # Page components (Login, Register, Profile, etc.)
│   │   ├── services/       # API service layer
│   │   └── contexts/       # React contexts (AuthContext)
│   └── package.json        # Node.js dependencies
├── README.md              # This file
└── TESTING.md             # Comprehensive testing guide
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework with automatic API documentation
- **Pydantic v2** - Data validation and serialization with comprehensive validation
- **JWT** - Secure token-based authentication
- **bcrypt** - Password hashing and verification
- **uvicorn** - ASGI server for production-ready deployment
- **pytest** - Comprehensive testing framework
- **pytest-asyncio** - Async testing support
- **pytest-cov** - Code coverage reporting

### Frontend
- **React 19** - Latest UI library with modern patterns
- **TypeScript** - Full type safety and better development experience
- **React Router v7** - Client-side routing with modern features
- **Vite** - Lightning-fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework for modern styling
- **React Context** - Global state management for authentication

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm** or **yarn**

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cosc4353-group-project
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd vite-project

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🧪 Testing

For comprehensive testing instructions, see [TESTING.md](./TESTING.md)

### Quick Test Commands

```bash
# Backend tests
cd backend
python -m pytest test_*.py -v
python -m pytest test_api_endpoints.py -v --cov=app

# Frontend tests (if configured)
cd vite-project
npm test
```

## 🔧 Development

### Backend Development

The backend follows a clean, modular architecture:

- **Models** (`app/models/`) - Pydantic v2 data models with comprehensive validation
- **Services** (`app/services/`) - Business logic and data operations with async support
- **API** (`app/api/`) - HTTP endpoints with proper error handling and validation
- **Utils** (`app/utils/`) - Shared utilities and custom exceptions

### Frontend Development

The frontend uses modern React patterns with TypeScript:

- **Components** (`src/components/`) - Reusable UI components with Tailwind CSS
- **Pages** (`src/pages/`) - Route-specific page components with proper error handling
- **Services** (`src/services/`) - Type-safe API communication layer
- **Contexts** (`src/contexts/`) - Global state management for authentication

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - User registration with validation
- `POST /auth/login` - User login with JWT token
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user information

### Profiles
- `POST /profile` - Create volunteer profile
- `GET /profile` - Get current user's profile
- `PUT /profile` - Update current user's profile
- `DELETE /profile` - Delete current user's profile

### Events
- `GET /events` - Get all available events
- `GET /events/{event_id}` - Get specific event details
- `POST /events` - Create new event (admin)
- `PUT /events/{event_id}` - Update event (admin)
- `DELETE /events/{event_id}` - Delete event (admin)

### Volunteer History
- `GET /history` - Get user's volunteer history
- `GET /history/stats` - Get user's volunteer statistics
- `POST /history/participate/{event_id}` - Join an event

### Matching System
- `POST /matching/signup/{event_id}` - Sign up for event matching
- `DELETE /matching/signup/{event_id}` - Cancel event signup
- `GET /matching/event/{event_id}/signups` - Get event signups
- `GET /matching/volunteer/signups` - Get user's signups

### Notifications
- `GET /notifications` - Get user's notifications
- `POST /notifications` - Create notification
- `PUT /notifications/{id}/read` - Mark notification as read
- `DELETE /notifications/{id}` - Delete notification

## 🔒 Security Features

- **JWT Authentication** - Secure token-based authentication with proper expiration
- **Password Hashing** - bcrypt for secure password storage and verification
- **Input Validation** - Comprehensive Pydantic v2 validation with custom error messages
- **CORS Configuration** - Proper cross-origin resource sharing setup
- **Error Handling** - Custom exceptions and proper HTTP status codes
- **Type Safety** - Full TypeScript integration for frontend security

## 🎨 UI/UX Features

- **Modern Design** - Clean, responsive interface with Tailwind CSS
- **Mobile Responsive** - Works seamlessly on all device sizes
- **Loading States** - Proper loading indicators and error handling
- **Form Validation** - Real-time validation with helpful error messages
- **Navigation** - Intuitive navigation with authentication-aware routing
- **Accessibility** - Proper ARIA labels and keyboard navigation

## 🚧 Current Status

### ✅ Completed (Phases 1-11)

#### Phase 1-3: Foundation
- ✅ Project structure and environment setup
- ✅ Basic FastAPI application with proper configuration
- ✅ CORS and middleware setup

#### Phase 4-6: Core Models & Services
- ✅ Comprehensive Pydantic v2 models with validation
- ✅ User authentication system with JWT
- ✅ Profile management with skills and availability
- ✅ Event management system
- ✅ Volunteer history tracking
- ✅ Notification system
- ✅ Matching algorithm

#### Phase 7-8: API Development
- ✅ Complete REST API with all endpoints
- ✅ Proper error handling and validation
- ✅ Authentication middleware
- ✅ API documentation with Swagger UI

#### Phase 9-10: Testing & Quality
- ✅ Comprehensive unit tests for all models
- ✅ API endpoint tests with authentication
- ✅ Code coverage reporting (>80% target)
- ✅ Error handling validation

#### Phase 11: Frontend Integration
- ✅ Modern React frontend with TypeScript
- ✅ Complete authentication flow (register, login, logout)
- ✅ Profile management interface
- ✅ Event browsing and joining
- ✅ Volunteer history and statistics
- ✅ Notification management
- ✅ Responsive design with Tailwind CSS
- ✅ Real-time API integration

### 🚧 In Progress
- Database integration (currently using in-memory storage)
- Advanced search and filtering
- Admin dashboard features
- Email notification system

### 📋 Planned (Future Phases)
- **Phase 12**: Database Integration (PostgreSQL/SQLite)
- **Phase 13**: Advanced Features (email, file uploads)
- **Phase 14**: Performance Optimization
- **Phase 15**: Deployment & Production Setup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the [TESTING.md](./TESTING.md) for detailed testing instructions
- Review the API documentation at `http://localhost:8000/docs`
- Open an issue in the repository

---

**Last Updated**: Phase 11 Complete - Frontend Integration ✅
