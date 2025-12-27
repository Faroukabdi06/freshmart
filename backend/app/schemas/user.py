from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    name : str
    email : EmailStr
    phone_number : str

class UserCreate(UserBase):
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str


class UserResponse(UserBase):
    id : UUID
    role : str
    created_at : datetime

    class Config:
        from_attributes = True
