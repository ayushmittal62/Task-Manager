from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str

class UserCreate(BaseModel):
    password: str
    role: str = "user"

class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    status: str = "pending"
    priority: str = "medium"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    status: str
    owner_id: int

    class Config:
        orm_mode = True

