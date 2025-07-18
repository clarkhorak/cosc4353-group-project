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
     - Username: `testuser`
     - Full Name: `Test User`
     - Email: `test@example.com`
     - Password: `TestPass123` (must include uppercase)
   - Click "Register"

3. **Login with the registered user:**
   - Username: `testuser`
   - Password: `TestPass123`
   - Click "Login"

4. **Create/Update Profile:**
   - Fill in your address information
   - Select skills (hold Ctrl/Cmd to select multiple)
   - Add availability dates and times
   - Add preferences (optional)
   - Click "Create Profile" or "Update Profile"

5. **Test Navigation:**
   - Navigate between different pages using the navbar
   - Verify that authentication persists across page refreshes

6. **Test Logout:**
   - Click logout or navigate to `/logout`
   - Verify you're redirected to the login page

### Expected Behavior

- ✅ Registration creates user in backend and redirects to login
- ✅ Login gets JWT token and updates authentication state
- ✅ Profile loads existing data or allows creation of new profile
- ✅ Protected routes work with authentication
- ✅ Logout clears token and redirects to login
- ✅ Error messages display properly for failed operations

## 🔧 Development

### Project Structure
```
src/
├── components/          # Reusable UI components
│   ├── Navbar.tsx      # Navigation component
│   └── AdminLink.tsx   # Admin-specific components
├── pages/              # Route-specific page components
│   ├── Login.tsx       # Login page
│   ├── Register.tsx    # Registration page
│   ├── Profile.tsx     # Profile management
│   └── ...             # Other pages
├── services/           # API communication
│   └── api.ts          # API service layer
├── contexts/           # React contexts
│   └── AuthContext.tsx # Authentication context
└── App.tsx             # Main application component
```

### Key Features

- **TypeScript**: Full type safety throughout the application
- **React Router**: Client-side routing with protected routes
- **Context API**: Global state management for authentication
- **API Integration**: Complete integration with FastAPI backend
- **Error Handling**: Comprehensive error handling and user feedback

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🔗 API Integration

The frontend communicates with the backend through the `api.ts` service layer:

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login  
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user

### Profile Endpoints
- `POST /profiles/` - Create profile
- `GET /profiles/me` - Get my profile
- `PUT /profiles/me` - Update my profile
- `DELETE /profiles/me` - Delete my profile
- `GET /profiles/` - Get all profiles
- `GET /profiles/search/skills` - Search by skills
- `GET /profiles/search/location` - Search by location

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

**Build errors:**
- Check TypeScript compilation errors
- Verify all imports are correct
- Ensure all required dependencies are installed

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
- Input validation is handled on both frontend and backend
- CORS is properly configured for development

## 🚧 Current Status

### ✅ Completed
- User authentication (login/register/logout)
- Profile management (create/read/update)
- API integration with backend
- Authentication context and state management
- Error handling and user feedback

### 🚧 In Progress
- Event management interface
- Volunteer matching interface
- Notification system
- Admin dashboard

### 📋 Planned
- Mobile responsiveness improvements
- Advanced search and filtering UI
- File upload for profile pictures
- Real-time notifications
- Progressive Web App features