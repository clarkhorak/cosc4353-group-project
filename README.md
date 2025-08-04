# Volunteer Management System

A full-stack web application for managing volunteer opportunities, built with React (Frontend) and FastAPI (Backend).

## 🚀 Project Overview

This system allows organizations to post volunteer events and volunteers to find opportunities that match their skills and availability. The application includes user authentication, profile management, event management, volunteer matching, and comprehensive notification systems with role-based access control.

## 📁 Project Structure

```
cosc4353-group-project/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints (auth, profile, events, history, matching, notifications)
│   │   ├── models/         # Pydantic data models and SQLAlchemy database models
│   │   ├── services/       # Business logic services
│   │   └── utils/          # Utilities and exceptions
│   ├── requirements.txt    # Python dependencies
│   ├── test_*.py          # Unit tests
│   └── test_api_endpoints.py # Comprehensive API tests
├── vite-project/           # React frontend
│   ├── src/
│   │   ├── components/     # React components (Navbar, etc.)
│   │   ├── pages/          # Page components (Login, Register, Profile, AdminDashboard, etc.)
│   │   ├── services/       # API service layer
│   │   └── contexts/       # React contexts (AuthContext)
│   └── package.json        # Node.js dependencies
├── README.md              # This file
└── TESTING.md             # Comprehensive testing guide
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework with automatic API documentation
- **SQLAlchemy** - Database ORM with PostgreSQL support
- **Pydantic v2** - Data validation and serialization
- **JWT** - Secure token-based authentication with role-based access
- **bcrypt** - Password hashing and verification
- **uvicorn** - ASGI server for production-ready deployment
- **pytest** - Comprehensive testing framework

### Frontend
- **React 19** - Latest UI library with modern patterns
- **TypeScript** - Full type safety and better development experience
- **React Router v7** - Client-side routing with protected routes
- **Vite** - Lightning-fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework for modern styling

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cosc4353-group-project
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt)
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd vite-project
npm install
npm run dev
```

## 🔑 Key Features

### ✅ Completed
- **Role-based Authentication**: Admin and volunteer user roles with proper access control
- **User Management**: Registration, login, profile management with state validation
- **Event Management**: Full CRUD operations with admin-only creation/editing
- **Volunteer Matching**: Intelligent matching algorithm with signup system
- **History Tracking**: Complete participation tracking and statistics
- **Notifications**: Real-time notification system
- **Admin Dashboard**: Comprehensive admin interface for managing events and users
- **Database Integration**: PostgreSQL with SQLAlchemy ORM and proper constraints

### 🚧 In Progress
- Email notification system
- File upload capabilities
- Advanced search and filtering

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - User registration with role assignment
- `POST /auth/login` - User login with JWT token
- `GET /auth/me` - Get current user information

### Admin Endpoints
- `GET /admin/users` - Get all users (admin only)
- `POST /admin/events` - Create events (admin only)
- `PUT /admin/events/{id}` - Update events (admin only)

### Profile & Events
- `POST /profile` - Create volunteer profile
- `GET /events` - Get all available events
- `GET /history` - Get user's volunteer history
- `GET /notifications` - Get user's notifications

## 🔒 Security Features

- **Role-based Access Control**: Admin and volunteer roles with proper permissions
- **JWT Authentication**: Secure token-based authentication
- **Input Validation**: Comprehensive validation with custom error messages
- **Database Constraints**: Proper foreign key relationships and data integrity

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest test_*.py -v

# Frontend testing
cd vite-project
npm run dev
# Manual testing through browser
```

## 🚧 Current Status

### ✅ Completed
- Role-based user management (admin/volunteer)
- Admin dashboard with user and event management
- Enhanced database schema with proper relationships
- State management for profiles
- Comprehensive API with role-based endpoints
- Frontend integration with admin features

### 📋 Planned
- Email notification system
- File upload capabilities
- Advanced search and filtering
- Performance optimization

## 🤝 Contributing

1. Follow the development plan and phase structure
2. Write comprehensive tests for new features
3. Ensure code coverage remains above 80%
4. Update documentation as needed

## 📞 Support

For detailed testing instructions, see [TESTING.md](./TESTING.md)
For API documentation, visit `http://localhost:8000/docs`

---

**Last Updated**: Role-based Access Control & Admin Dashboard ✅
