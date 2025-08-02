# Volunteer Management System - Frontend

React-based frontend for the Volunteer Management System, built with TypeScript and Vite.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Installation
```bash
cd vite-project
npm install
```

### Development Server
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## 🧪 Testing the Frontend

### Prerequisites
Make sure the backend server is running first:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Manual Testing Flow

1. **Open the application** at `http://localhost:5173`

2. **Register a new user:**
   - Click "Register here" on the login page
   - Fill in the registration form:
     - Email: `test@example.com`
     - Full Name: `Test User`
     - Password: `TestPass123` (must include uppercase)
   - Click "Register"

3. **Login with the registered user:**
   - Email: `test@example.com`
   - Password: `TestPass123`
   - Click "Login"

4. **Create/Update Profile:**
   - Fill in your address information
   - Select state from dropdown
   - Select skills (hold Ctrl/Cmd to select multiple)
   - Add availability dates and times
   - Add preferences (optional)
   - Click "Create Profile" or "Update Profile"

5. **Test Admin Features (if admin role):**
   - Navigate to Admin Dashboard
   - Create and manage events
   - View all users

6. **Test Navigation:**
   - Navigate between different pages using the navbar
   - Verify that authentication persists across page refreshes

### Expected Behavior

- ✅ Registration creates user in backend and redirects to login
- ✅ Login gets JWT token and updates authentication state
- ✅ Profile loads existing data or allows creation of new profile
- ✅ Protected routes work with authentication
- ✅ Admin dashboard accessible only to admin users
- ✅ Role-based navigation and features

## 🔧 Development

### Project Structure
```
src/
├── components/          # Reusable UI components
│   └── Navbar.tsx      # Navigation component with role-based links
├── pages/              # Route-specific page components
│   ├── Login.tsx       # Login page
│   ├── Register.tsx    # Registration page
│   ├── Profile.tsx     # Profile management with state validation
│   ├── AdminDashboard.tsx # Admin interface for managing events/users
│   └── ...             # Other pages
├── services/           # API communication
│   └── api.ts          # API service layer
├── contexts/           # React contexts
│   └── AuthContext.tsx # Authentication context with role management
└── App.tsx             # Main application component
```

### Key Features

- **TypeScript**: Full type safety throughout the application
- **React Router**: Client-side routing with protected routes
- **Context API**: Global state management for authentication and roles
- **API Integration**: Complete integration with FastAPI backend
- **Role-based UI**: Different interfaces for admin and volunteer users

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🔗 API Integration

The frontend communicates with the backend through the `api.ts` service layer:

### Authentication Endpoints
- `POST /auth/register` - User registration with role assignment
- `POST /auth/login` - User login  
- `GET /auth/me` - Get current user with role information

### Admin Endpoints
- `GET /admin/users` - Get all users (admin only)
- `POST /admin/events` - Create events (admin only)
- `PUT /admin/events/{id}` - Update events (admin only)

### Profile Endpoints
- `POST /profile` - Create profile with state validation
- `GET /profile` - Get my profile
- `PUT /profile` - Update my profile

## 🆘 Troubleshooting

### Common Issues

**Frontend won't start:**
- Ensure Node.js 16+ is installed
- Check that all dependencies are installed: `npm install`
- Verify you're in the `vite-project` directory

**API calls failing:**
- Ensure the backend server is running on port 8000
- Check browser console for detailed error messages
- Verify CORS configuration in backend

**Authentication issues:**
- Check that JWT token is stored in localStorage
- Verify token format in browser dev tools
- Ensure backend authentication is working

**Admin features not working:**
- Verify user has admin role in backend
- Check role-based routing in frontend
- Ensure admin endpoints are properly protected

### Debugging

1. **Check browser console** for JavaScript errors
2. **Check Network tab** for failed API requests
3. **Check Application tab** for localStorage issues
4. **Check backend logs** for server-side errors

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🔒 Security Notes

- JWT tokens are stored in localStorage
- All API calls include proper authentication headers
- Role-based access control implemented
- Input validation handled on both frontend and backend

## 🚧 Current Status

### ✅ Completed
- User authentication (login/register) with role assignment
- Profile management with state validation
- Admin dashboard with user and event management
- Role-based navigation and access control
- API integration with backend
- Authentication context and state management

### 🚧 In Progress
- Enhanced event management interface
- Advanced volunteer matching interface
- Real-time notification system
- Mobile responsiveness improvements

### 📋 Planned
- Advanced search and filtering UI
- File upload for profile pictures
- Real-time notifications
- Progressive Web App features