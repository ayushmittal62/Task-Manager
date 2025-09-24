# Task Manager API

A RESTful Task Management API built with FastAPI, SQLAlchemy, and SQLite. This application provides user management and task management functionality with role-based access control.

## 🚀 Features

- **User Management**: User registration and retrieval
- **Task Management**: Create, read, update, and delete tasks
- **Role-Based Access Control**: Admin and regular user permissions
- **Database**: SQLite database with SQLAlchemy ORM
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Data Validation**: Pydantic schemas for request/response validation

## 📋 Project Structure

```
Task Manager/
├── readme.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── task_manager.db              # SQLite database
├── backend/
│   ├── main.py                  # FastAPI application entry point
│   ├── db/
│   │   ├── database.py          # Database connection and session management
│   │   ├── models.py            # SQLAlchemy database models
│   │   ├── schemas.py           # Pydantic schemas for API validation
│   │   ├── main.py              # Database initialization script
│   │   └── test_db.py           # Database inspection utility
│   └── CRUD/
│       ├── crud_operations.py   # Database CRUD operations
│       └── test_crud_fixed.py   # CRUD operations testing script
└── frontend/                    # (Empty - Future frontend implementation)
```

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
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
   pip install fastapi uvicorn sqlalchemy pydantic
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

### User Endpoints

#### Create User
- **POST** `/users/`
- **Description**: Register a new user
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "password": "secure_password",
    "role": "user"  // "user" or "admin"
  }
  ```
- **Response**: User object with ID and role

#### Get User by Username
- **GET** `/users/{username}`
- **Description**: Retrieve user information by username
- **Response**: User object with ID and role

### Task Endpoints

#### Create Task
- **POST** `/tasks/`
- **Description**: Create a new task
- **Query Parameters**:
  - `user_id` (required): ID of the task owner
- **Request Body**:
  ```json
  {
    "title": "Complete project documentation",
    "status": "pending",    // Default: "pending"
    "priority": "high"      // Default: "medium"
  }
  ```

#### Get Tasks
- **GET** `/tasks/`
- **Description**: Get tasks (admin sees all, users see only their own)
- **Query Parameters**:
  - `username` (required): Username to filter tasks
- **Response**: Array of task objects

#### Update Task
- **PUT** `/tasks/{task_id}`
- **Description**: Update task status and/or priority
- **Query Parameters**:
  - `username` (required): Username for permission check
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
- **Query Parameters**:
  - `username` (required): Username for permission check
- **Response**: Deleted task object

## 🗄️ Database Schema

### Users Table
| Column   | Type    | Description                    |
|----------|---------|--------------------------------|
| id       | Integer | Primary key                    |
| username | String  | Unique username                |
| password | String  | User password (plain text)     |
| role     | String  | User role ("user" or "admin")  |

### Tasks Table
| Column   | Type    | Description                    |
|----------|---------|--------------------------------|
| id       | Integer | Primary key                    |
| title    | String  | Task title                     |
| status   | String  | Task status (default: "pending") |
| priority | String  | Task priority (default: "medium") |
| owner_id | Integer | Foreign key to users.id       |

## 🔐 Access Control

### User Roles
- **Admin**: Can view, update, and delete all tasks
- **User**: Can only manage their own tasks

### Permission Matrix
| Action | Admin | User |
|--------|-------|------|
| Create User | ✅ | ✅ |
| View All Users | ✅ | ❌ |
| Create Task | ✅ | ✅ |
| View All Tasks | ✅ | Own only |
| Update Any Task | ✅ | Own only |
| Delete Any Task | ✅ | Own only |

## 🧪 Testing

### Run CRUD Tests
```bash
python backend/CRUD/test_crud_fixed.py
```

### Check Database Tables
```bash
python backend/db/test_db.py
```

### Test API Endpoints
Use the interactive docs at http://localhost:8000/docs or tools like Postman/curl.

## 🔧 Configuration

### Database Configuration
- **File**: `backend/db/database.py`
- **Database URL**: `sqlite:///./task_manager.db`
- **Connection**: SQLite with thread safety disabled

### Application Configuration
- **File**: `backend/main.py`
- **Title**: "Task Manager API"
- **Auto-reload**: Enabled in development

## 🚨 Known Issues & Security Considerations

⚠️ **Security Warning**: This is a development version with the following limitations:

1. **Password Security**: Passwords are stored as plain text (not hashed)
2. **Authentication**: No JWT or session-based authentication implemented
3. **Input Validation**: Basic validation only
4. **Error Handling**: Limited error handling and logging
5. **Rate Limiting**: No rate limiting implemented

## 🔮 Future Enhancements

- [ ] JWT Authentication
- [ ] Password hashing (bcrypt)
- [ ] Frontend implementation
- [ ] Task due dates and reminders
- [ ] Task categories and tags
- [ ] File attachments
- [ ] Team collaboration features
- [ ] Email notifications
- [ ] Database migrations
- [ ] Docker containerization
- [ ] API rate limiting
- [ ] Comprehensive logging

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

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request successful |
| 400 | Bad Request - Invalid input |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |

---

**Happy Task Managing! 🎯**