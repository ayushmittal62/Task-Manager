from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.db import models, database, schemas
from backend.CRUD import crud_operations as crud
from backend.jwt_auth import verify_token, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Task Manager API with JWT Authentication")

# Security scheme
security = HTTPBearer()

def get_db():
    """Database dependency"""
    db = database.Sessionlocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Extract token
    token = credentials.credentials
    username = verify_token(token)
    
    if username is None:
        raise credentials_exception
    
    # Get user from database
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user

# ===== AUTHENTICATION ENDPOINTS =====

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login endpoint - returns JWT token"""
    user = crud.authenticate_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ===== USER ENDPOINTS =====

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user.username, user.password, user.role)

@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """Get current user info"""
    return current_user

@app.get("/users/{username}", response_model=schemas.UserResponse)
def read_user(
    username: str, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get user by username (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_user = crud.get_user_by_username(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# ===== TASK ENDPOINTS (ALL NOW REQUIRE AUTHENTICATION) =====

@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new task"""
    return crud.create_task(db, task.title, task.priority, current_user.id)

@app.get("/tasks/", response_model=list[schemas.TaskResponse])
def read_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all tasks (admin sees all, users see only their own)"""
    return crud.get_all_tasks(db, current_user)

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int, 
    task: schemas.TaskUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update a task"""
    updated = crud.update_task_admin_only(db, task_id, current_user, task.status, task.priority)
    if updated == "Not Allowed":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@app.delete("/tasks/{task_id}", response_model=schemas.TaskResponse)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a task"""
    deleted = crud.delete_task_admin_only(db, task_id, current_user)
    if deleted == "Not Allowed":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if deleted is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted