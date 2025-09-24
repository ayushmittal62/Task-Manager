from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db import models, database, schemas
from backend.CRUD import crud_operations as crud

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Task Manager API")

def get_db():
    db = database.Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user.username, user.password, user.role)

@app.get("/users/{username}", response_model=schemas.UserResponse)
def read_user(username: str, db: Session = Depends(get_db)):
    db_user= crud.get_user_by_username(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_task(db, task.title, task.priority, user_id)

@app.get("/tasks/", response_model=list[schemas.TaskResponse])
def read_tasks(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_all_tasks(db, user)

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskUpdate, username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated = crud.update_task_admin_only(db, task_id, user, task.status, task.priority)
    if updated == "Not Allowed":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@app.delete("/tasks/{task_id}", response_model=schemas.TaskResponse)
def delete_task(task_id: int, username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    deleted = crud.delete_task_admin_only(db, task_id, user)
    if deleted == "Not Allowed":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if deleted is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted
