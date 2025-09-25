# Task Manager API with JWT Authentication

A secure RESTful Task Management API built with FastAPI, SQLAlchemy, JWT authentication, and SQLite. This application provides comprehensive user management and task management functionality with enterprise-grade security and role-based access control.

## 🚀 Features

- **🔐 JWT Authentication**: Secure token-based authentication with Bearer tokens
- **🛡️ Password Security**: BCrypt password hashing for secure storage
- **👥 User Management**: User registration, authentication, and profile management
- **📋 Task Management**: Create, read, update, and delete tasks with full CRUD operations
- **🔑 Role-Based Access Control**: Admin and regular user permissions with granular access
- **🏗️ Database**: SQLite database with SQLAlchemy ORM and proper relationships
- **📚 API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **✅ Data Validation**: Comprehensive Pydantic schemas for request/response validation
- **⏰ Token Expiration**: Configurable JWT token expiration (30 minutes default)

## 📋 Project Structure

```
Task Manager/
├── readme.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── task_manager.db              # SQLite database
├── backend/
│   ├── main.py                  # FastAPI application with JWT endpoints
│   ├── jwt_auth.py              # JWT token management and password hashing
│   ├── dependencies.py          # Authentication dependencies (if created)
│   ├── db/
│   │   ├── database.py          # Database connection and session management
│   │   ├── models.py            # SQLAlchemy database models (User & Task)
│   │   ├── schemas.py           # Pydantic schemas for API validation
│   │   ├── main.py              # Database initialization script
│   │   └── test_db.py           # Database inspection utility
│   └── CRUD/
│       ├── crud_operations.py   # Database CRUD operations with auth
│       └── test_crud_fixed.py   # CRUD operations testing script
└── frontend/                    # (Empty - Future frontend implementation)
```

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **Authentication**: JWT (JSON Web Tokens) with Bearer token
- **Password Hashing**: BCrypt via Passlib
- **Database**: SQLite with SQLAlchemy ORM
- **Data Validation**: Pydantic v2
- **API Documentation**: OpenAPI/Swagger
- **Python Version**: 3.8+

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

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
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python -m backend.db.main
   ```

5. **Run the application**
   ```bash
   uvicorn backend.main:app --reload
   ```

6. **Access the API**
   - API Server: http://localhost:8000
   - Interactive API Docs: http://localhost:8000/docs
   - Alternative API Docs: http://localhost:8000/redoc

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

## 🔐 Authentication Flow

### 1. User Registration
```http
POST /users/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password123",
  "role": "user"  // "user" or "admin"
}
```

### 2. User Login (Get JWT Token)
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

### 3. Using Protected Endpoints
All task endpoints require authentication. Include the JWT token in the Authorization header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 📋 API Endpoints

### Authentication Endpoints

#### Login
- **POST** `/token`
- **Description**: Authenticate user and receive JWT token
- **Request Body**: `{"username": "string", "password": "string"}`
- **Response**: JWT token with 30-minute expiration

### User Endpoints

#### Register User
- **POST** `/users/`
- **Description**: Register a new user
- **Authentication**: Not required
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
- **Response**: Current user object

#### Get User by Username
- **GET** `/users/{username}`
- **Description**: Get user information by username (admin only)
- **Authentication**: Required (Admin role)
- **Response**: User object

### Task Endpoints (All Require Authentication)

#### Create Task
- **POST** `/tasks/`
- **Description**: Create a new task
- **Authentication**: Required (JWT token)
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
- **Response**: Array of task objects

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

## 🧪 Testing

### Using Swagger UI (Recommended)
1. Visit http://localhost:8000/docs
2. Register a user using `POST /users/`
3. Login using `POST /token` to get JWT token
4. Click "Authorize" button and enter: `Bearer YOUR_TOKEN`
5. Test protected endpoints

### Using cURL
```bash
# Register user
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass", "role": "user"}'

# Login
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# Create task (replace TOKEN with actual token)
curl -X POST "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "priority": "high"}'
```

### Run CRUD Tests
```bash
python backend/CRUD/test_crud_fixed.py
```

## 📊 Access Control Matrix

| Action           | Admin | User      | Anonymous |
|------------------|-------|-----------|-----------|
| Register User    | ✅    | ✅        | ✅        |
| Login            | ✅    | ✅        | ❌        |
| View Own Profile | ✅    | ✅        | ❌        |
| View All Users   | ✅    | ❌        | ❌        |
| Create Task      | ✅    | ✅        | ❌        |
| View All Tasks   | ✅    | Own only  | ❌        |
| Update Any Task  | ✅    | Own only  | ❌        |
| Delete Any Task  | ✅    | Own only  | ❌        |

## 📁 Dependencies

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
python-multipart>=0.0.6
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0
pydantic>=2.0.0
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

## 🔮 Future Enhancements

- [ ] Refresh token implementation
- [ ] Email verification for user registration
- [ ] Password reset functionality
- [ ] Frontend React/Vue.js application
- [ ] Task due dates and reminders
- [ ] Task categories and tags
- [ ] File attachments for tasks
- [ ] Team collaboration features
- [ ] Email notifications
- [ ] Database migrations with Alembic
- [ ] Docker containerization
- [ ] API rate limiting and throttling
- [ ] Comprehensive audit logging
- [ ] OAuth2 integration (Google, GitHub)

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

**🎯 Your Task Manager with Enterprise-Grade JWT Authentication is Ready!** 🔐✨