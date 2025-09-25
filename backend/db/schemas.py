from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):  # Now inherits from UserBase to include username
    password: str
    role: str = "user"

class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

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
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    username: Optional[str] = None

