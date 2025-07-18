# Volunteer Management System - Backend

This is the backend API for the Volunteer Management System, built with FastAPI and Python.

## Features

- **Authentication**: JWT-based authentication with bcrypt password hashing
- **User Management**: Profile creation, updates, and management
- **Event Management**: Create, update, and manage volunteer events
- **Volunteer Matching**: Intelligent matching algorithm based on skills and availability
- **Notifications**: Real-time notifications for volunteers and administrators
- **History Tracking**: Complete volunteer participation history and statistics

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Authentication**: JWT with bcrypt
- **Validation**: Pydantic
- **Testing**: Pytest with coverage
- **Documentation**: Auto-generated OpenAPI/Swagger

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

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

1. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Running Tests

1. **Run all tests:**
   ```bash
   pytest
   ```

2. **Run tests with coverage:**
   ```bash
   pytest --cov=app --cov-report=html
   ```

3. **Run specific test categories:**
   ```bash
   pytest -m auth      # Authentication tests
   pytest -m users     # User management tests
   pytest -m events    # Event management tests
   ```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative API docs**: http://localhost:8000/redoc

## Development

### Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── models/              # Pydantic data models
│   ├── services/            # Business logic services
│   ├── api/                 # API route handlers
│   └── utils/               # Utility functions
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── pytest.ini             # Test configuration
```

### Code Quality

- Follow PEP 8 style guidelines
- Use type hints throughout
- Write comprehensive docstrings
- Maintain >80% test coverage

## Environment Variables

Create a `.env` file in the backend directory with:

```env
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here
```

## Contributing

1. Follow the development plan in `BACKEND_DEVELOPMENT_PLAN.md`
2. Write tests for new features
3. Ensure code coverage remains above 80%
4. Update documentation as needed 