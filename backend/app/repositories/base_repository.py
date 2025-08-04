from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from app.database import get_session_local
from app.models.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Base repository class for common database operations"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get_session(self) -> Session:
        """Get database session"""
        SessionLocal = get_session_local()
        return SessionLocal()
    
    def create(self, **kwargs) -> ModelType:
        """Create a new record"""
        session = self.get_session()
        try:
            db_obj = self.model(**kwargs)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_by_id(self, id: str) -> Optional[ModelType]:
        """Get record by ID"""
        session = self.get_session()
        try:
            stmt = select(self.model).where(self.model.id == id)
            result = session.execute(stmt)
            obj = result.scalar_one_or_none()
            if obj:
                session.refresh(obj)
            return obj
        finally:
            session.close()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination"""
        session = self.get_session()
        try:
            stmt = select(self.model).offset(skip).limit(limit)
            result = session.execute(stmt)
            objects = result.scalars().all()
            # Refresh all objects to ensure they're loaded before session closes
            for obj in objects:
                session.refresh(obj)
            return objects
        finally:
            session.close()
    
    def update(self, id: str, **kwargs) -> Optional[ModelType]:
        """Update record by ID"""
        session = self.get_session()
        try:
            stmt = update(self.model).where(self.model.id == id).values(**kwargs)
            result = session.execute(stmt)
            session.commit()
            if result.rowcount > 0:
                return self.get_by_id(id)
            return None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self, id: str) -> bool:
        """Delete record by ID"""
        session = self.get_session()
        try:
            stmt = delete(self.model).where(self.model.id == id)
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def exists(self, id: str) -> bool:
        """Check if record exists"""
        return self.get_by_id(id) is not None 