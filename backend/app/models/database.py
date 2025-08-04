from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey, Table, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

# Association tables for many-to-many relationships
user_skills = Table(
    'user_skills',
    Base.metadata,
    Column('user_id', String, ForeignKey('users.id')),
    Column('skill', String)
)

user_availability = Table(
    'user_availability',
    Base.metadata,
    Column('user_id', String, ForeignKey('users.id')),
    Column('date', String),
    Column('time', String)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="volunteer")  # Added role field
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Database constraints
    __table_args__ = (
        CheckConstraint("length(full_name) >= 2", name="full_name_min_length"),
        CheckConstraint("length(full_name) <= 50", name="full_name_max_length"),
        CheckConstraint(r"email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'", name="valid_email_format"),
        CheckConstraint("role IN ('volunteer', 'admin')", name="valid_user_role"),  # Added role constraint
    )
    
    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False)
    events_created = relationship("Event", back_populates="created_by")
    participations = relationship("History", back_populates="user")
    signups = relationship("Matching", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    address1 = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state_code = Column(String(2), ForeignKey("states.code"), nullable=False)  # Changed from state to state_code with FK
    zip_code = Column(String, nullable=False)
    skills = Column(Text)  # JSON string of skills
    availability = Column(Text)  # JSON string of availability
    preferences = Column(Text)  # User preferences
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Database constraints
    __table_args__ = (
        CheckConstraint("length(address1) >= 5", name="address_min_length"),
        CheckConstraint("length(address1) <= 100", name="address_max_length"),
        CheckConstraint("length(city) >= 2", name="city_min_length"),
        CheckConstraint("length(city) <= 50", name="city_max_length"),
        CheckConstraint("zip_code ~ '^[0-9]{5}(-[0-9]{4})?$'", name="valid_zip_format"),
    )
    
    # Relationships
    user = relationship("User", back_populates="profile")
    state = relationship("State", back_populates="profiles")  # Added relationship to State

class Event(Base):
    __tablename__ = "events"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    requirements = Column(Text)
    required_skills = Column(Text)  # JSON string of required skills
    category = Column(String, nullable=False)
    urgency = Column(String, default="Medium")  # Low, Medium, High
    event_date = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String, default="open")
    created_by_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Database constraints
    __table_args__ = (
        CheckConstraint("length(title) >= 3", name="title_min_length"),
        CheckConstraint("length(title) <= 100", name="title_max_length"),
        CheckConstraint("length(location) >= 3", name="location_min_length"),
        CheckConstraint("length(location) <= 200", name="location_max_length"),
        CheckConstraint("capacity >= 1", name="capacity_min"),
        CheckConstraint("capacity <= 10000", name="capacity_max"),
        CheckConstraint("urgency IN ('Low', 'Medium', 'High')", name="valid_urgency"),
        CheckConstraint("status IN ('open', 'closed', 'cancelled')", name="valid_status"),
    )
    
    # Relationships
    created_by = relationship("User", back_populates="events_created")
    participations = relationship("History", back_populates="event")
    signups = relationship("Matching", back_populates="event")

class History(Base):
    __tablename__ = "history"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    participation_date = Column(String, nullable=False)
    hours_volunteered = Column(Integer, default=0)
    status = Column(String, default="completed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Database constraints
    __table_args__ = (
        CheckConstraint("hours_volunteered >= 0", name="hours_non_negative"),
        CheckConstraint("status IN ('completed', 'cancelled', 'no_show')", name="valid_participation_status"),
    )
    
    # Relationships
    user = relationship("User", back_populates="participations")
    event = relationship("Event", back_populates="participations")

class Matching(Base):
    __tablename__ = "matching"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    signup_date = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Database constraints
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'approved', 'rejected', 'cancelled')", name="valid_signup_status"),
    )
    
    # Relationships
    user = relationship("User", back_populates="signups")
    event = relationship("Event", back_populates="signups")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String, default="info")
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Database constraints
    __table_args__ = (
        CheckConstraint("length(title) >= 1", name="notification_title_min_length"),
        CheckConstraint("length(title) <= 100", name="notification_title_max_length"),
        CheckConstraint("type IN ('info', 'warning', 'error', 'success')", name="valid_notification_type"),
    )
    
    # Relationships
    user = relationship("User", back_populates="notifications")

class State(Base):
    __tablename__ = "states"
    
    code = Column(String(2), primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    profiles = relationship("Profile", back_populates="state") 