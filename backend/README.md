# Volunteer Management System - Backend

This is the backend API for the Volunteer Management System, built with FastAPI and Python.

## 🚀 Features

### ✅ Completed
- **Role-based Authentication**: Admin and volunteer user roles with proper access control
- **User Management**: Complete user registration, login, and profile management
- **Profile System**: Comprehensive profile creation with state validation
- **Event Management**: Full CRUD operations with admin-only creation/editing
- **Volunteer History**: Complete participation tracking and statistics
- **Matching System**: Intelligent volunteer-event matching algorithm
- **Notifications**: Real-time notification system
- **Admin Dashboard**: Comprehensive admin interface for managing events and users
- **Database Integration**: PostgreSQL with SQLAlchemy ORM and proper constraints
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Comprehensive Testing**: Unit tests, API tests, and >80% code coverage

### 🚧 In Progress
- Email notification system
- File upload capabilities
- Performance optimization

## 🛠️ Tech Stack

- **Framework**: FastAPI with automatic API documentation
- **Language**: Python 3.8+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with role-based access control
- **Validation**: Pydantic v2 with comprehensive validation
- **Testing**: Pytest with async support and coverage reporting

## 📋 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL database

### Installation
```bash
cd backend
python -m venv venv
# Activate virtual environment
pip install -r requirements.txt
```

### Running the Application
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the application:
- Backend API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs

### Running Tests
```bash
# All tests with coverage
python -m pytest test_*.py --cov=app --cov-report=html

# Individual test files
python test_auth.py
python test_profile.py
python test_event.py
```

## 📚 API Documentation

### Authentication Endpoints
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

## 🔧 Development

### Project Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── models/              # Pydantic v2 data models and SQLAlchemy models
│   ├── services/            # Business logic services
│   ├── api/                 # API route handlers
│   └── utils/               # Utilities and exceptions
├── test_*.py               # Unit test files
└── requirements.txt        # Python dependencies
```

## 🔒 Security Features

- **Role-based Access Control**: Admin and volunteer roles with proper permissions
- **JWT Authentication**: Secure token-based authentication
- **Input Validation**: Comprehensive Pydantic v2 validation
- **Database Constraints**: Proper foreign key relationships and data integrity

## 🚧 Current Status

### ✅ Completed
- Role-based user management (admin/volunteer)
- Admin dashboard with user and event management
- Enhanced database schema with proper relationships
- State management for profiles
- Comprehensive API with role-based endpoints

### 📋 Planned
- Email notification system
- File upload capabilities
- Advanced search and filtering
- Performance optimization

## 📞 Support

For detailed testing instructions, see [TESTING.md](../TESTING.md)
For API documentation, visit `http://localhost:8000/docs`

---

**Last Updated**: Role-based Access Control & Admin Dashboard ✅ 