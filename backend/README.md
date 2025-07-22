# Volunteer Management System - Backend

This is the backend API for the Volunteer Management System, built with FastAPI and Python.

## 🚀 Features

### ✅ Completed (Phases 1-11)
- **Authentication**: JWT-based authentication with bcrypt password hashing
- **User Management**: Complete user registration, login, and profile management
- **Profile System**: Comprehensive profile creation, updates, and validation
- **Event Management**: Full CRUD operations for volunteer events
- **Volunteer History**: Complete participation tracking and statistics
- **Matching System**: Intelligent volunteer-event matching algorithm
- **Notifications**: Real-time notification system for volunteers
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Comprehensive Testing**: Unit tests, API tests, and >80% code coverage
- **Frontend Integration**: Complete React frontend with real-time API integration

### 🚧 In Progress
- **Database Integration**: Moving from in-memory to persistent storage
- **Advanced Features**: Email notifications, file uploads
- **Performance Optimization**: Caching and query optimization

## 🛠️ Tech Stack

- **Framework**: FastAPI with automatic API documentation
- **Language**: Python 3.8+
- **Authentication**: JWT with bcrypt password hashing
- **Validation**: Pydantic v2 with comprehensive validation
- **Testing**: Pytest with async support and coverage reporting
- **Documentation**: Auto-generated OpenAPI/Swagger UI
- **Frontend**: React 19 with TypeScript and Tailwind CSS

## 📋 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Node.js 16+ (for frontend)

### Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the backend server:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the frontend server (in a new terminal):**
   ```bash
   cd vite-project
   npm install
   npm run dev
   ```

3. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Running Tests

#### 1. Model Tests
```bash
python test_models.py
```

#### 2. API Endpoint Tests
```bash
python -m pytest test_api_endpoints.py -v
```

#### 3. All Tests with Coverage
```bash
python -m pytest test_*.py --cov=app --cov-report=html --cov-report=term
```

#### 4. Individual Test Files
```bash
python test_auth.py
python test_profile.py
python test_event.py
python test_history.py
python test_matching.py
python test_notification.py
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/register` - User registration with validation
- `POST /auth/login` - User login with JWT token
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user information

### Profile Endpoints
- `POST /profile` - Create volunteer profile
- `GET /profile` - Get current user's profile
- `PUT /profile` - Update current user's profile
- `DELETE /profile` - Delete current user's profile

### Event Endpoints
- `GET /events` - Get all available events
- `GET /events/{event_id}` - Get specific event details
- `POST /events` - Create new event (admin)
- `PUT /events/{event_id}` - Update event (admin)
- `DELETE /events/{event_id}` - Delete event (admin)

### History Endpoints
- `GET /history` - Get user's volunteer history
- `GET /history/stats` - Get user's volunteer statistics
- `POST /history/participate/{event_id}` - Join an event

### Matching Endpoints
- `POST /matching/signup/{event_id}` - Sign up for event matching
- `DELETE /matching/signup/{event_id}` - Cancel event signup
- `GET /matching/event/{event_id}/signups` - Get event signups
- `GET /matching/volunteer/signups` - Get user's signups

### Notification Endpoints
- `GET /notifications` - Get user's notifications
- `POST /notifications` - Create notification
- `PUT /notifications/{id}/read` - Mark notification as read
- `DELETE /notifications/{id}` - Delete notification

## 🔧 Development

### Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── models/              # Pydantic v2 data models
│   │   ├── user.py          # User authentication models
│   │   ├── profile.py       # Profile management models
│   │   ├── event.py         # Event management models
│   │   ├── history.py       # Volunteer history models
│   │   └── notification.py  # Notification models
│   ├── services/            # Business logic services
│   │   ├── auth_service.py      # Authentication logic
│   │   ├── profile_service.py   # Profile management
│   │   ├── event_service.py     # Event management
│   │   ├── history_service.py   # History tracking
│   │   ├── matching_service.py  # Volunteer matching
│   │   └── notification_service.py # Notifications
│   ├── api/                 # API route handlers
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── profile.py       # Profile endpoints
│   │   ├── event.py         # Event endpoints
│   │   ├── history.py       # History endpoints
│   │   ├── matching.py      # Matching endpoints
│   │   └── notification.py  # Notification endpoints
│   └── utils/               # Utility functions
│       └── exceptions.py    # Custom exceptions
├── test_*.py               # Unit test files
├── test_api_endpoints.py   # Comprehensive API tests
├── requirements.txt        # Python dependencies
└── pytest.ini            # Test configuration
```

### Code Quality Standards

- **PEP 8** style guidelines
- **Type hints** throughout all functions
- **Comprehensive docstrings** for all public functions
- **>80% test coverage** maintained
- **Async/await** patterns for all I/O operations
- **Pydantic v2** validation for all data models

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication with proper expiration
- **Password Hashing**: bcrypt for secure password storage and verification
- **Input Validation**: Comprehensive Pydantic v2 validation with custom error messages
- **CORS Configuration**: Proper cross-origin resource sharing setup
- **Error Handling**: Custom exceptions and proper HTTP status codes
- **Type Safety**: Full type checking with mypy support

## 🧪 Testing Strategy

### Test Coverage
- **Unit Tests**: All models, services, and utilities
- **API Tests**: All endpoints with authentication
- **Integration Tests**: End-to-end user flows
- **Validation Tests**: All Pydantic model validations

### Test Commands
```bash
# Run all tests
python -m pytest test_*.py -v

# Run with coverage
python -m pytest test_*.py --cov=app --cov-report=html

# Run specific test file
python -m pytest test_auth.py -v

# Run API tests only
python -m pytest test_api_endpoints.py -v
```

## 📊 Current Status

### ✅ Completed Phases

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
- ✅ Complete authentication flow integration
- ✅ Real-time API communication
- ✅ Responsive design with Tailwind CSS

### 🚧 Next Phases
- **Phase 12**: Database Integration (PostgreSQL/SQLite)
- **Phase 13**: Advanced Features (email, file uploads)
- **Phase 14**: Performance Optimization
- **Phase 15**: Deployment & Production Setup

## 🌐 Frontend Integration

The backend is fully integrated with a modern React frontend:

- **Real-time API Communication**: All endpoints connected
- **Authentication Flow**: Complete login/register/logout
- **Profile Management**: Full CRUD operations
- **Event Browsing**: Browse and join events
- **History Tracking**: View volunteer history and statistics
- **Notifications**: Real-time notification management

## 🐛 Troubleshooting

### Common Issues

**Server won't start:**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID> /F
```

**Import errors:**
```bash
# Ensure you're in the backend directory
cd backend

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Test failures:**
```bash
# Run tests with verbose output
python -m pytest test_*.py -v -s

# Check specific test file
python -m pytest test_auth.py -v -s
```

**Frontend connection issues:**
```bash
# Check if backend is running
curl http://localhost:8000/docs

# Check CORS configuration
# Verify API_BASE_URL in frontend
```

## 📝 Environment Variables

Create a `.env` file in the backend directory with:

```env
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🤝 Contributing

1. Follow the development plan and phase structure
2. Write comprehensive tests for new features
3. Ensure code coverage remains above 80%
4. Update documentation as needed
5. Follow PEP 8 and type hint guidelines

## 📞 Support

For detailed testing instructions, see [TESTING.md](../TESTING.md)
For API documentation, visit `http://localhost:8000/docs`
For issues, open a ticket in the repository

---

**Last Updated**: Phase 11 Complete - Full Stack Integration ✅ 