from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import date, time
import re

class Address(BaseModel):
    """Address model with validation"""
    address1: str
    address2: Optional[str] = None
    city: str
    state_code: str  # Changed from state to state_code
    zip_code: str
    
    @field_validator('address1')
    @classmethod
    def validate_address1(cls, v):
        if len(v.strip()) < 5:
            raise ValueError('Address must be at least 5 characters')
        if len(v) > 100:
            raise ValueError('Address cannot exceed 100 characters')
        return v.strip()
    
    @field_validator('city')
    @classmethod
    def validate_city(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('City must be at least 2 characters')
        if len(v) > 50:
            raise ValueError('City cannot exceed 50 characters')
        return v.strip()
    
    @field_validator('state_code')  # Updated validator name
    @classmethod
    def validate_state_code(cls, v):  # Updated method name
        if len(v.strip()) != 2:
            raise ValueError('State code must be 2 characters (e.g., TX, CA)')
        return v.strip().upper()
    
    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, v):
        if not re.match(r'^\d{5}(-\d{4})?$', v):
            raise ValueError('Zip code must be 5 digits or 5+4 format (e.g., 12345 or 12345-6789)')
        return v

class Availability(BaseModel):
    """Availability time slot model"""
    date: date
    time: time
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v < date.today():
            raise ValueError('Availability date cannot be in the past')
        return v

class Profile(BaseModel):
    """Complete user profile model"""
    user_id: str
    address: Address
    skills: List[str]
    preferences: Optional[str] = None
    availability: List[Availability]
    
    @field_validator('skills')
    @classmethod
    def validate_skills(cls, v):
        if not v:
            raise ValueError('At least one skill must be selected')
        if len(v) > 10:
            raise ValueError('Cannot select more than 10 skills')
        
        # Validate against predefined skill list
        valid_skills = {
            'First Aid', 'Teaching', 'Cooking', 'Driving', 'Organizing',
            'Technical Support', 'Childcare', 'Elderly Care', 'Translation',
            'Event Planning', 'Fundraising', 'Marketing', 'Photography',
            'Videography', 'Music', 'Art', 'Sports', 'Tutoring'
        }
        
        invalid_skills = [skill for skill in v if skill not in valid_skills]
        if invalid_skills:
            raise ValueError(f'Invalid skills: {", ".join(invalid_skills)}')
        
        return v
    
    @field_validator('preferences')
    @classmethod
    def validate_preferences(cls, v):
        if v and len(v) > 500:
            raise ValueError('Preferences cannot exceed 500 characters')
        return v
    
    @field_validator('availability')
    @classmethod
    def validate_availability(cls, v):
        if not v:
            raise ValueError('At least one availability slot must be provided')
        
        # Check for duplicate date/time combinations
        availability_set = set()
        for avail in v:
            avail_key = (avail.date, avail.time)
            if avail_key in availability_set:
                raise ValueError('Duplicate availability entry found')
            availability_set.add(avail_key)
        
        return v

class ProfileCreate(BaseModel):
    """Profile creation model"""
    address: Address
    skills: List[str]
    preferences: Optional[str] = None
    availability: List[Availability]

class ProfileUpdate(BaseModel):
    """Profile update model (all fields optional)"""
    address: Optional[Address] = None
    skills: Optional[List[str]] = None
    preferences: Optional[str] = None
    availability: Optional[List[Availability]] = None 