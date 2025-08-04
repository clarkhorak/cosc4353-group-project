from functools import wraps
from fastapi import HTTPException, status, Depends
from app.models.user import User
from app.api.auth import get_current_user
from typing import Callable, Any

def admin_required(func: Callable) -> Callable:
    """
    Decorator to require admin role for endpoint access.
    Usage: @admin_required
    """
    @wraps(func)
    async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs) -> Any:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        return await func(*args, current_user=current_user, **kwargs)
    return wrapper

def volunteer_required(func: Callable) -> Callable:
    """
    Decorator to require volunteer role for endpoint access.
    Usage: @volunteer_required
    """
    @wraps(func)
    async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs) -> Any:
        if current_user.role != "volunteer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Volunteer access required"
            )
        return await func(*args, current_user=current_user, **kwargs)
    return wrapper

def role_required(allowed_roles: list[str]):
    """
    Decorator factory to require specific roles for endpoint access.
    Usage: @role_required(["admin", "volunteer"])
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs) -> Any:
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

def get_user_role(current_user: User = Depends(get_current_user)) -> str:
    """
    Dependency to get current user's role.
    Usage: role: str = Depends(get_user_role)
    """
    return current_user.role

def is_admin(current_user: User = Depends(get_current_user)) -> bool:
    """
    Dependency to check if current user is admin.
    Usage: is_admin_user: bool = Depends(is_admin)
    """
    return current_user.role == "admin"

def is_volunteer(current_user: User = Depends(get_current_user)) -> bool:
    """
    Dependency to check if current user is volunteer.
    Usage: is_volunteer_user: bool = Depends(is_volunteer)
    """
    return current_user.role == "volunteer" 