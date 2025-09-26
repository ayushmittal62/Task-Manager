# Task Manager - Full Stack Application with JWT Authentication

A comprehensive full-stack Task Management application featuring a FastAPI backend with JWT authentication and a modern Streamlit frontend. This enterprise-grade application provides secure user management, role-based access control, and intuitive task management with real-time updates.

## 🚀 Features

### 🔐 Authentication & Security
- **JWT Authentication**: Secure token-based authentication with Bearer tokens
- **Password Security**: BCrypt password hashing for secure credential storage
- **Role-Based Access Control**: Admin and user roles with granular permissions
- **Session Management**: Streamlit session state integration with JWT tokens
- **Token Expiration**: Configurable JWT token expiration (30 minutes default)

### 👥 User Management
- **User Registration**: Self-registration with role selection
- **User Authentication**: Secure login with session persistence
- **Admin Panel**: Complete user management (view, create, delete users)
- **Profile Management**: View current user information
- **Access Control**: Admin-only operations protection

### 📋 Task Management
- **Full CRUD Operations**: Create, read, update, and delete tasks
- **Status Management**: Track task progress (pending, in-progress, completed)
- **Priority Levels**: Organize tasks by priority (low, medium, high)
- **Real-time Updates**: Instant UI refresh after operations
- **Personal & Admin Views**: Users see own tasks, admins see all tasks

### �️ Modern UI Features
- **Streamlit Frontend**: Modern, responsive web interface
- **Dashboard**: Overview with task statistics and quick actions
- **Navigation**: Intuitive sidebar navigation with role-based menus
- **Real-time Feedback**: Success/error messages with operation status
- **Form Validation**: Client-side input validation and error handling

### 🏗️ Technical Excellence
- **SQLite Database**: Lightweight database with SQLAlchemy ORM
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Data Validation**: Comprehensive Pydantic schemas
- **Error Handling**: Robust error handling with informative messages

## 📋 Project Structure

```
Task Manager/
├── readme.md                    # Comprehensive project documentation
├── requirements.txt             # Python dependencies (backend + frontend)
├── task_manager.db              # SQLite database file
├── backend/                     # FastAPI Backend
│   ├── main.py                  # FastAPI application with JWT endpoints
│   ├── jwt_auth.py              # JWT token management and password hashing
│   ├── db/
│   │   ├── database.py          # Database connection and session management
│   │   ├── models.py            # SQLAlchemy database models (User & Task)
│   │   ├── schemas.py           # Pydantic schemas for API validation
│   │   ├── main.py              # Database initialization script
│   │   └── test_db.py           # Database inspection utility
│   └── CRUD/
│       ├── crud_operations.py   # Database CRUD operations with authentication
│       └── test_crud_fixed.py   # CRUD operations testing script
└── frontend/                    # Streamlit Frontend
    ├── app.py                   # Main Streamlit application
    ├── api.py                   # API communication layer
    ├── auth.py                  # Authentication helpers & session management
    └── pages/                   # Individual page components
        ├── login.py             # Login page component
        ├── dashboard.py         # Dashboard page component  
        ├── tasks.py             # Task management page component
        └── admin.py             # Admin panel page component
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.104.0+
- **Server**: Uvicorn ASGI server
- **Authentication**: JWT (JSON Web Tokens) with Bearer tokens
- **Password Hashing**: BCrypt via Passlib
- **Database**: SQLite with SQLAlchemy ORM 2.0+
- **Data Validation**: Pydantic v2
- **API Documentation**: OpenAPI/Swagger

### Frontend
- **Framework**: Streamlit 1.28.0+
- **HTTP Client**: Requests 2.31.0+
- **Session Management**: Streamlit session state
- **UI Components**: Native Streamlit components
- **Real-time Updates**: Streamlit rerun functionality

### Database & Security
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **ORM**: SQLAlchemy 2.0+ with relationship mapping
- **Migration Support**: Alembic ready
- **Encryption**: Cryptography package for enhanced security
- **Testing**: Pytest with async support

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Quick Start Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/ayushmittal62/Task-Manager.git
   cd Task-Manager
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   # On Windows PowerShell
   venv\Scripts\Activate.ps1
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install all dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database** (optional - auto-created on first run)
   ```bash
   python -m backend.db.main
   ```

5. **Start the Backend Server**
   ```bash
   # Navigate to backend directory
   cd backend
   python main.py
   ```
   Backend will be available at: http://localhost:8000

6. **Start the Frontend Application** (in a new terminal)
   ```bash
   # Navigate to frontend directory (from project root)
   cd frontend
   streamlit run app.py
   ```
   Frontend will be available at: http://localhost:8501

### 🌐 Access Points
- **Frontend UI**: http://localhost:8501 (Main user interface)
- **Backend API**: http://localhost:8000 (REST API)
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc (ReDoc)

## 🖥️ User Interface Guide

### Getting Started
1. **Open the Frontend**: Navigate to http://localhost:8501
2. **Register**: Create a new account (choose 'admin' role for full access)
3. **Login**: Use your credentials to access the dashboard
4. **Explore**: Navigate through Dashboard, Tasks, and Admin Panel

### Dashboard Features
- **📊 Task Statistics**: Overview of total, completed, and pending tasks
- **🚀 Quick Actions**: Fast access to create tasks and manage users
- **📈 Progress Tracking**: Visual representation of task completion

### Task Management
- **➕ Create Tasks**: Add new tasks with title and priority
- **📝 Update Status**: Change task status (pending → in-progress → completed)
- **🗑️ Delete Tasks**: Remove completed or unwanted tasks
- **🎯 Priority Management**: Set task priorities (low, medium, high)

### Admin Panel (Admin Users Only)
- **👥 User Management**: View all registered users
- **🔧 Create Users**: Add new users with specific roles
- **🗑️ Delete Users**: Remove users (cannot delete yourself)
- **📊 System Overview**: Monitor system-wide task statistics

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication Flow

The application uses JWT (JSON Web Token) authentication. Here's how to authenticate:

1. **Register** a new user via the frontend or API
2. **Login** to receive a JWT token
3. **Include the token** in the Authorization header for protected endpoints

## 🔐 Complete Authentication Guide

### User Registration (Frontend)
1. Open http://localhost:8501
2. Use the registration form on the login page
3. Choose username, password, and role (user/admin)
4. Click "Register" to create your account

### User Registration (API)
```http
POST /users/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password123",
  "role": "user"  // "user" or "admin"
}
```

### User Login (API)
```http
POST /token
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using Protected Endpoints
Include the JWT token in the Authorization header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 📋 Complete API Reference

### Authentication Endpoints

#### Login
- **POST** `/token`
- **Description**: Authenticate user and receive JWT token
- **Request Body**: `{"username": "string", "password": "string"}`
- **Response**: JWT token with 30-minute expiration
- **Status Codes**: 200 (Success), 401 (Invalid credentials)

### User Management Endpoints

#### Register User
- **POST** `/users/`
- **Description**: Register a new user
- **Authentication**: Not required
- **Status Code**: 201 (Created)
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "password": "secure_password123",
    "role": "user"
  }
  ```

#### Get Current User
- **GET** `/users/me`
- **Description**: Get current authenticated user information
- **Authentication**: Required (JWT token)
- **Response**: Current user object with id, username, and role

#### Get All Users (Admin Only)
- **GET** `/users/`
- **Description**: Get all registered users
- **Authentication**: Required (Admin role)
- **Response**: Array of user objects

#### Get User by Username (Admin Only)
- **GET** `/users/{username}`
- **Description**: Get user information by username
- **Authentication**: Required (Admin role)
- **Response**: User object

#### Delete User (Admin Only)
- **DELETE** `/users/{user_id}`
- **Description**: Delete user by ID (cannot delete yourself)
- **Authentication**: Required (Admin role)
- **Response**: Deletion confirmation message

### Task Management Endpoints (All Require Authentication)

#### Create Task
- **POST** `/tasks/`
- **Description**: Create a new task
- **Authentication**: Required (JWT token)
- **Status Code**: 201 (Created)
- **Request Body**:
  ```json
  {
    "title": "Complete project documentation",
    "status": "pending",    // Optional, default: "pending"
    "priority": "high"      // Optional, default: "medium"
  }
  ```

#### Get Tasks
- **GET** `/tasks/`
- **Description**: Get tasks (admin sees all, users see only their own)
- **Authentication**: Required (JWT token)
- **Response**: Array of task objects with id, title, status, priority, owner_id

#### Update Task
- **PUT** `/tasks/{task_id}`
- **Description**: Update task status and/or priority
- **Authentication**: Required (JWT token, own tasks or admin)
- **Request Body**:
  ```json
  {
    "status": "completed",  // Optional
    "priority": "low"       // Optional
  }
  ```

#### Delete Task
- **DELETE** `/tasks/{task_id}`
- **Description**: Delete a task
- **Authentication**: Required (JWT token, own tasks or admin)
- **Response**: Deleted task object

## 🗄️ Database Schema

### Users Table
| Column          | Type    | Description                      |
|-----------------|---------|----------------------------------|
| id              | Integer | Primary key                      |
| username        | String  | Unique username                  |
| hashed_password | String  | BCrypt hashed password           |
| role            | String  | User role ("user" or "admin")    |

### Tasks Table
| Column   | Type    | Description                         |
|----------|---------|-------------------------------------|
| id       | Integer | Primary key                         |
| title    | String  | Task title                          |
| status   | String  | Task status (default: "pending")   |
| priority | String  | Task priority (default: "medium")  |
| owner_id | Integer | Foreign key to users.id            |

## 🔐 Security Features

### JWT Token Security
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration**: 30 minutes (configurable)
- **Secret Key**: Cryptographically secure random key
- **Token Format**: Standard Bearer token

### Password Security
- **Hashing Algorithm**: BCrypt with salt
- **Plain Text Storage**: Never stored
- **Verification**: Secure password verification

### Access Control
- **Authentication**: Required for all task operations
- **Authorization**: Role-based permissions (admin/user)
- **Token Validation**: Automatic token verification

## 🔧 Configuration

### JWT Configuration (`backend/jwt_auth.py`)
```python
SECRET_KEY = "your-secure-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### Database Configuration (`backend/db/database.py`)
```python
DATABASE_URL = "sqlite:///./task_manager.db"
```

## 🧪 Testing & Development

### Using the Frontend (Recommended)
1. **Access Streamlit UI**: http://localhost:8501
2. **Register Admin**: Create account with admin role
3. **Test Features**: Use the intuitive web interface to test all functionality
4. **Real-time Feedback**: Observe immediate UI updates after operations

### Using Swagger UI (API Testing)
1. **Access Swagger**: http://localhost:8000/docs
2. **Register User**: Use `POST /users/` endpoint
3. **Login**: Use `POST /token` to get JWT token
4. **Authorize**: Click "Authorize" button and enter: `Bearer YOUR_TOKEN`
5. **Test Endpoints**: Explore all available API endpoints

### Using cURL (Command Line)
```bash
# Register user
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass", "role": "admin"}'

# Login and get token
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# Create task (replace TOKEN with actual token)
curl -X POST "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "priority": "high"}'

# Get all tasks
curl -X GET "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer TOKEN"
```

### Running Backend Tests
```bash
# Run CRUD operation tests
python backend/CRUD/test_crud_fixed.py

# Check database content
python backend/db/test_db.py
```

### Development Mode
```bash
# Backend with auto-reload
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend with auto-reload (automatic)
cd frontend
streamlit run app.py
```

## 📊 Enhanced Access Control Matrix

| Action                    | Admin | User      | Anonymous |
|---------------------------|-------|-----------|-----------|
| **Authentication**        |       |           |           |
| Register User             | ✅    | ✅        | ✅        |
| Login                     | ✅    | ✅        | ❌        |
| Logout                    | ✅    | ✅        | ❌        |
| **User Management**       |       |           |           |
| View Own Profile          | ✅    | ✅        | ❌        |
| View All Users            | ✅    | ❌        | ❌        |
| Create Users              | ✅    | ❌        | ❌        |
| Delete Other Users        | ✅    | ❌        | ❌        |
| **Task Management**       |       |           |           |
| Create Task               | ✅    | ✅        | ❌        |
| View All Tasks            | ✅    | Own only  | ❌        |
| Update Any Task           | ✅    | Own only  | ❌        |
| Delete Any Task           | ✅    | Own only  | ❌        |
| **Frontend Features**     |       |           |           |
| Dashboard Access          | ✅    | ✅        | ❌        |
| Admin Panel Access        | ✅    | ❌        | ❌        |
| Task Statistics           | ✅    | ✅        | ❌        |
| User Management UI        | ✅    | ❌        | ❌        |

## 📁 Updated Dependencies

```txt
# FastAPI Backend Dependencies
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
python-multipart>=0.0.6
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0
pydantic>=2.0.0

# Streamlit Frontend Dependencies
streamlit>=1.28.0
requests>=2.31.0

# Database Dependencies
sqlite3  # Built-in with Python
alembic>=1.12.0

# Additional Security & Utility Packages
bcrypt>=4.0.1
cryptography>=41.0.0
pytz>=2023.3

# Development & Testing (Optional)
pytest>=7.4.0
pytest-asyncio>=0.21.0
httpx>=0.25.0
```

## 🚨 Security Considerations

### ✅ Implemented Security Features
- BCrypt password hashing
- JWT token authentication
- Token expiration (30 minutes)
- Role-based access control
- Input validation with Pydantic
- CORS protection (configurable)

### ⚠️ Production Recommendations
1. **Change SECRET_KEY**: Use a cryptographically secure random key
2. **Use HTTPS**: Enable SSL/TLS in production
3. **Environment Variables**: Store secrets in environment variables
4. **Database Security**: Use PostgreSQL/MySQL in production
5. **Rate Limiting**: Implement API rate limiting
6. **Logging**: Add comprehensive security logging
7. **Token Refresh**: Consider implementing refresh tokens

## 🔮 Roadmap & Future Enhancements

### ✅ Completed Features
- [x] JWT Authentication with secure token management
- [x] Role-based access control (Admin/User)
- [x] Complete CRUD operations for tasks and users
- [x] Modern Streamlit frontend with real-time updates
- [x] Admin panel with user management
- [x] Dashboard with task statistics
- [x] Secure password hashing with BCrypt
- [x] Session state management
- [x] API documentation with Swagger/OpenAPI

### 🚧 In Progress
- [ ] Enhanced error handling and validation
- [ ] Improved UI/UX design and styling
- [ ] Database migration scripts
- [ ] Comprehensive test suite

### 🎯 Planned Features
- [ ] **Authentication Enhancements**
  - [ ] Refresh token implementation
  - [ ] Email verification for user registration
  - [ ] Password reset functionality
  - [ ] Two-factor authentication (2FA)
  - [ ] OAuth2 integration (Google, GitHub, Microsoft)

- [ ] **Task Management Improvements**
  - [ ] Task due dates and deadlines
  - [ ] Task categories and tags
  - [ ] File attachments for tasks
  - [ ] Task comments and notes
  - [ ] Task templates
  - [ ] Bulk task operations

- [ ] **Collaboration Features**
  - [ ] Team/workspace management
  - [ ] Task assignment to team members
  - [ ] Real-time collaboration
  - [ ] Activity feeds and notifications
  - [ ] Task sharing and permissions

- [ ] **Advanced Features**
  - [ ] Email notifications and reminders
  - [ ] Calendar integration
  - [ ] Time tracking functionality
  - [ ] Task dependencies and workflows
  - [ ] Gantt chart visualization
  - [ ] Progress reporting and analytics

- [ ] **Technical Improvements**
  - [ ] PostgreSQL database support
  - [ ] Redis caching layer
  - [ ] Docker containerization
  - [ ] Kubernetes deployment configs
  - [ ] API rate limiting and throttling
  - [ ] Comprehensive audit logging
  - [ ] Performance monitoring
  - [ ] Automated testing pipeline
  - [ ] Load balancing support

- [ ] **Frontend Enhancements**
  - [ ] Dark/light theme toggle
  - [ ] Mobile-responsive design
  - [ ] Progressive Web App (PWA) support
  - [ ] Offline functionality
  - [ ] Advanced data visualization
  - [ ] Export functionality (PDF, Excel)
  - [ ] Drag-and-drop task management
  - [ ] Keyboard shortcuts

- [ ] **Alternative Frontend Options**
  - [ ] React.js frontend implementation
  - [ ] Vue.js frontend implementation
  - [ ] Mobile app (React Native/Flutter)
  - [ ] Desktop app (Electron)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Contact

- **GitHub**: [@ayushmittal62](https://github.com/ayushmittal62)
- **Repository**: [Task-Manager](https://github.com/ayushmittal62/Task-Manager)

## 📈 API Status Codes

| Status Code | Description                    |
|-------------|--------------------------------|
| 200         | OK - Request successful        |
| 201         | Created - Resource created     |
| 400         | Bad Request - Invalid input    |
| 401         | Unauthorized - Authentication required |
| 403         | Forbidden - Insufficient permissions |
| 404         | Not Found - Resource not found |
| 422         | Unprocessable Entity - Validation error |
| 500         | Internal Server Error         |

---

## 🏆 Key Highlights

- **🔐 Enterprise Security**: JWT authentication with BCrypt password hashing
- **🎨 Modern UI**: Streamlit-powered frontend with intuitive navigation  
- **👥 Role Management**: Comprehensive admin panel for user management
- **📊 Real-time Dashboard**: Live task statistics and progress tracking
- **🔄 Instant Updates**: Real-time UI refresh after all operations
- **📚 Auto Documentation**: Swagger/OpenAPI documentation
- **🛡️ Access Control**: Granular permissions based on user roles
- **💾 Persistent Sessions**: Secure session management with JWT tokens

**🎯 Your Full-Stack Task Manager with Enterprise-Grade Security is Ready!** �✨

---

*Built with ❤️ using FastAPI, Streamlit, and modern Python development practices.*