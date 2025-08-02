from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
import re

class UserBase(BaseModel):
    """Base user model with common fields"""
    email: EmailStr
    full_name: str
    role: str = "volunteer"  # Added role field with default
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters')
        if len(v) > 50:
            raise ValueError('Full name cannot exceed 50 characters')
        if not re.match(r'^[a-zA-Z\s]+$', v.strip()):
            raise ValueError('Full name can only contain letters and spaces')
        return v.strip()
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v not in ['volunteer', 'admin']:
            raise ValueError('Role must be either "volunteer" or "admin"')
        return v

class UserCreate(UserBase):
    """User registration model"""
    password: str
    
    @field_validator('password')
    @classmethod
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
    
    model_config = {
        "from_attributes": True
    }

class UserResponse(BaseModel):
    """User response model (without sensitive data)"""
    id: str
    email: EmailStr
    full_name: str
    role: str  # Added role field
    created_at: datetime
    is_active: bool
    
    model_config = {
        "from_attributes": True
    } 