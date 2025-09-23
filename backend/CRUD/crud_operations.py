from backend.db import models
from sqlalchemy.orm import Session

def create_user(db: Session, username:str , password: str, role: str = "user"):
    db_user = models.User(username=username, password=password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_task(db: Session, title: str, priority: str, user_id: int):
    db_task = models.Task(title=title, priority=priority, owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_all_tasks(db: Session, user):
    if user.role == "admin":
        return db.query(models.Task).all()
    else:
        return db.query(models.Task).filter(models.Task.owner_id == user.id).all()
    

def update_task_admin_only(db: Session, task_id: int, user, status: str = None, priority: str = None):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        return None
    
    if user.role != "admin" and task.owner_id != user.id:
        return "Not Allowed"
    
    if status:
        task.status = status
    if priority:
        task.priority = priority

    db.commit()
    db.refresh(task)    
    return task


def delete_task_admin_only(db: Session, task_id: int, user):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        return None
    
    if user.role != "admin" and task.owner_id != user.id:
        return "Not Allowed"
    
    db.delete(task)
    db.commit()
    return task

