from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
import re

class UserBase(BaseModel):
    """Base user model with common fields"""
    email: EmailStr
    full_name: str
    
    @validator('full_name')
    def validate_full_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters')
        if len(v) > 50:
            raise ValueError('Full name cannot exceed 50 characters')
        if not re.match(r'^[a-zA-Z\s]+$', v.strip()):
            raise ValueError('Full name can only contain letters and spaces')
        return v.strip()

class UserCreate(UserBase):
    """User registration model"""
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str

class User(UserBase):
    """Complete user model with metadata"""
    id: str
    created_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    """User response model (without sensitive data)"""
    id: str
    email: EmailStr
    full_name: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True 