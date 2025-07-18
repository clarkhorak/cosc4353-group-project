class ProfileNotFoundError(Exception):
    """Raised when a profile is not found"""
    pass


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass


class AuthorizationError(Exception):
    """Raised when user is not authorized to perform an action"""
    pass


class EventNotFoundError(Exception):
    """Raised when an event is not found"""
    pass


class NotificationNotFoundError(Exception):
    """Raised when a notification is not found"""
    pass 