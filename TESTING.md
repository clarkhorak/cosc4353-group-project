# Testing Guide - Volunteer Management System

This document provides comprehensive testing instructions for the Volunteer Management System, covering both backend and frontend testing.

## 📋 Table of Contents

- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [Integration Testing](#integration-testing)
- [API Testing](#api-testing)
- [Manual Testing Scenarios](#manual-testing-scenarios)
- [Troubleshooting](#troubleshooting)

## 🧪 Backend Testing

### Prerequisites

```bash
cd backend
pip install -r requirements.txt
```

### Running Tests

#### 1. Model Tests
Test all Pydantic models and validation:

```bash
python test_models.py
```

**Expected Output:**
```
🚀 Starting Model Tests

🧪 Testing User Models...
✅ UserBase validation passed
✅ UserCreate validation passed
✅ UserLogin validation passed
✅ User validation passed
✅ UserResponse validation passed

🧪 Testing Profile Models...
✅ Address validation passed
✅ Availability validation passed
✅ Profile validation passed
✅ ProfileCreate validation passed
✅ ProfileUpdate validation passed

🧪 Testing Event Models...
✅ EventBase validation passed
✅ EventCreate validation passed
✅ EventResponse validation passed
✅ EventUpdate validation passed

🧪 Testing Notification Models...
✅ NotificationBase validation passed
✅ NotificationCreate validation passed
✅ Notification validation passed
✅ NotificationResponse validation passed

🧪 Testing History Models...
✅ ParticipationStatus enum validation passed
✅ VolunteerHistoryBase validation passed
✅ VolunteerHistoryCreate validation passed
✅ VolunteerHistory validation passed
✅ VolunteerStats validation passed

🧪 Testing Validation Errors...
✅ Invalid email validation working
✅ Short password validation working
✅ Invalid zip code validation working
✅ Empty skills validation working
✅ All validation error tests passed

🎉 All model tests passed!
```

#### 2. API Endpoint Tests
Test all API endpoints with authentication:

```bash
python -m pytest test_api_endpoints.py -v
```

**Expected Output:**
```
test_auth_endpoints[test_register_user] PASSED
test_auth_endpoints[test_login_user] PASSED
test_auth_endpoints[test_get_current_user] PASSED
test_profile_endpoints[test_create_profile] PASSED
test_profile_endpoints[test_get_profile] PASSED
test_profile_endpoints[test_update_profile] PASSED
test_event_endpoints[test_get_events] PASSED
test_event_endpoints[test_create_event] PASSED
test_event_endpoints[test_get_event] PASSED
test_event_endpoints[test_update_event] PASSED
test_event_endpoints[test_delete_event] PASSED
test_history_endpoints[test_get_history] PASSED
test_history_endpoints[test_get_stats] PASSED
test_history_endpoints[test_participate_in_event] PASSED
test_matching_endpoints[test_signup_for_event] PASSED
test_matching_endpoints[test_cancel_signup] PASSED
test_matching_endpoints[test_get_event_signups] PASSED
test_matching_endpoints[test_get_volunteer_signups] PASSED
test_notification_endpoints[test_get_notifications] PASSED
test_notification_endpoints[test_create_notification] PASSED
test_notification_endpoints[test_mark_notification_read] PASSED
test_notification_endpoints[test_delete_notification] PASSED
```

#### 3. Code Coverage
Run tests with coverage reporting:

```bash
python -m pytest test_*.py --cov=app --cov-report=html --cov-report=term
```

**Expected Output:**
```
---------- coverage: platform win32, python 3.12.0-final-0 -----------
Name                           Stmts   Miss  Cover
--------------------------------------------------
app/__init__.py                    0      0   100%
app/api/__init__.py                0      0   100%
app/api/auth.py                  185      0   100%
app/api/event.py                  95      0   100%
app/api/history.py                85      0   100%
app/api/matching.py               75      0   100%
app/api/notification.py           65      0   100%
app/api/profile.py                95      0   100%
app/config.py                     15      0   100%
app/main.py                       25      0   100%
app/models/__init__.py             0      0   100%
app/models/event.py               45      0   100%
app/models/history.py             35      0   100%
app/models/notification.py        35      0   100%
app/models/profile.py             45      0   100%
app/models/user.py                65      0   100%
app/services/__init__.py           0      0   100%
app/services/auth_service.py     125      0   100%
app/services/event_service.py     85      0   100%
app/services/history_service.py   75      0   100%
app/services/matching_service.py  65      0   100%
app/services/notification_service.py 55      0   100%
app/services/profile_service.py   85      0   100%
app/utils/__init__.py              0      0   100%
app/utils/exceptions.py           15      0   100%
--------------------------------------------------
TOTAL                           1155      0   100%
```

### Individual Test Files

#### Authentication Tests
```bash
python test_auth.py
```

#### Profile Tests
```bash
python test_profile.py
```

#### Event Tests
```bash
python test_event.py
```

#### History Tests
```bash
python test_history.py
```

#### Matching Tests
```bash
python test_matching.py
```

#### Notification Tests
```bash
python test_notification.py
```

## 🌐 Frontend Testing

### Prerequisites

```bash
cd vite-project
npm install
```

### Running Tests

#### 1. Unit Tests (if configured)
```bash
npm test
```

#### 2. Build Test
```bash
npm run build
```

#### 3. Linting
```bash
npm run lint
```

## 🔗 Integration Testing

### Full Stack Testing

1. **Start Backend Server:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. **Start Frontend Server:**
```bash
cd vite-project
npm run dev
```

3. **Test Complete User Flow:**
   - Open `http://localhost:5173`
   - Register a new user
   - Login with credentials
   - Create/update profile
   - Browse events
   - Join events
   - View history and notifications

## 🔌 API Testing

### Using Swagger UI

1. Start the backend server
2. Visit `http://localhost:8000/docs`
3. Test endpoints interactively

### Using curl Commands

#### Authentication

**Register User:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123",
    "full_name": "Test User"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

**Get Current User (with token):**
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Profile Management

**Create Profile:**
```bash
curl -X POST "http://localhost:8000/profile" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "address": {
      "address1": "123 Main St",
      "city": "Houston",
      "state": "TX",
      "zip_code": "77001"
    },
    "skills": ["Teaching", "First Aid", "Organizing"],
    "availability": [
      {"date": "2025-12-25", "time": "09:00:00"},
      {"date": "2025-12-26", "time": "14:00:00"}
    ]
  }'
```

**Get Profile:**
```bash
curl -X GET "http://localhost:8000/profile" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Event Management

**Get All Events:**
```bash
curl -X GET "http://localhost:8000/events" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Create Event:**
```bash
curl -X POST "http://localhost:8000/events" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Community Cleanup",
    "description": "Help clean up the local park",
    "category": "Environment",
    "event_date": "2025-12-25",
    "start_time": "09:00:00",
    "end_time": "12:00:00",
    "location": "Central Park, Houston, TX",
    "capacity": 100,
    "status": "open"
  }'
```

## 👥 Manual Testing Scenarios

### Scenario 1: New User Registration and Profile Setup

**Steps:**
1. Open `http://localhost:5173`
2. Click "Register here"
3. Fill in registration form:
   - Full Name: "John Doe"
   - Email: "john@example.com"
   - Password: "TestPass123"
4. Submit registration
5. Login with credentials
6. Navigate to Profile page
7. Create profile with:
   - Address: "123 Oak St, Houston, TX 77001"
   - Skills: ["Teaching", "First Aid"]
   - Availability: Add 2-3 time slots
8. Save profile

**Expected Results:**
- ✅ Registration successful
- ✅ Login successful
- ✅ Profile created and saved
- ✅ Data persists after page refresh

### Scenario 2: Event Browsing and Participation

**Prerequisites:** Complete Scenario 1

**Steps:**
1. Login to the application
2. Navigate to "Events" page
3. Browse available events
4. Click "Join Event" on an event
5. Navigate to "History" page
6. Verify event appears in history

**Expected Results:**
- ✅ Events display correctly
- ✅ Join button works
- ✅ Event appears in volunteer history
- ✅ Statistics update correctly

### Scenario 3: Notification System

**Prerequisites:** Complete Scenarios 1 & 2

**Steps:**
1. Login to the application
2. Navigate to "Notifications" page
3. Check for any notifications
4. Mark notifications as read
5. Delete a notification

**Expected Results:**
- ✅ Notifications display correctly
- ✅ Mark as read functionality works
- ✅ Delete functionality works
- ✅ UI updates appropriately

### Scenario 4: Profile Management

**Prerequisites:** Complete Scenario 1

**Steps:**
1. Login to the application
2. Navigate to "Profile" page
3. Update profile information:
   - Change address
   - Add/remove skills
   - Modify availability
4. Save changes
5. Refresh page and verify changes persist

**Expected Results:**
- ✅ Profile updates save correctly
- ✅ Changes persist after refresh
- ✅ Validation works for all fields
- ✅ Error messages display appropriately

### Scenario 5: Authentication Flow

**Steps:**
1. Open application in incognito/private window
2. Try to access protected pages (Profile, Events, etc.)
3. Verify redirect to login page
4. Login with valid credentials
5. Verify access to protected pages
6. Test logout functionality
7. Verify redirect to login page after logout

**Expected Results:**
- ✅ Protected routes redirect to login
- ✅ Login grants access to protected pages
- ✅ Logout clears authentication
- ✅ Proper redirects after logout

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues

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

#### Frontend Issues

**Build errors:**
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for TypeScript errors
npx tsc --noEmit
```

**API connection errors:**
```bash
# Check if backend is running
curl http://localhost:8000/docs

# Check CORS configuration
# Verify API_BASE_URL in src/services/api.ts
```

#### Authentication Issues

**Login fails:**
- Verify password meets requirements (uppercase, lowercase, number, 8+ chars)
- Check browser console for detailed error messages
- Verify backend server is running

**Token issues:**
- Clear browser localStorage: `localStorage.clear()`
- Check token format in browser dev tools
- Verify token expiration

### Debug Mode

#### Backend Debug
```bash
# Run with debug logging
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

#### Frontend Debug
```bash
# Open browser dev tools
# Check Console tab for errors
# Check Network tab for API calls
# Check Application tab for localStorage
```

### Performance Testing

#### Load Testing (Optional)
```bash
# Install Apache Bench (if available)
ab -n 100 -c 10 http://localhost:8000/docs

# Or use Python for simple load testing
python -c "
import requests
import time
start = time.time()
for i in range(100):
    requests.get('http://localhost:8000/docs')
print(f'Average response time: {(time.time() - start) / 100:.3f}s')
"
```

## 📊 Test Results

### Expected Coverage
- **Backend**: >80% code coverage
- **Frontend**: All components render without errors
- **API**: All endpoints return correct responses
- **Integration**: Complete user flows work end-to-end

### Test Checklist

- [ ] All model validations pass
- [ ] All API endpoints respond correctly
- [ ] Authentication flow works
- [ ] Profile CRUD operations work
- [ ] Event management works
- [ ] History tracking works
- [ ] Notifications work
- [ ] Frontend components render
- [ ] Navigation works
- [ ] Error handling works
- [ ] Mobile responsiveness works

## 📝 Test Data

### Sample Users
```json
{
  "email": "admin@example.com",
  "password": "AdminPass123",
  "full_name": "Admin User"
}
```

```json
{
  "email": "volunteer@example.com",
  "password": "VolunteerPass123",
  "full_name": "Volunteer User"
}
```

### Sample Events
```json
{
  "title": "Community Cleanup",
  "description": "Help clean up the local park",
  "category": "Environment",
  "event_date": "2025-12-25",
  "start_time": "09:00:00",
  "end_time": "12:00:00",
  "location": "Central Park, Houston, TX",
  "capacity": 100,
  "status": "open"
}
```

---

**Last Updated**: Phase 11 Complete - Comprehensive Testing Guide ✅ 