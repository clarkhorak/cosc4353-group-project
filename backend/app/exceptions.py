
class ProfileNotFoundError(Exception):
    """Raised when a profile is not found"""
    def __init__(self, profile_id=None, message=None):
        if message is None:
            if profile_id is not None:
                message = f"Profile with id '{profile_id}' was not found."
            else:
                message = "Profile was not found."
        super().__init__(message)
    pass


class ValidationError(Exception):
    """Raised when validation fails"""

    def __init__(self, message="Validation failed.", errors=None):
        if errors is not None:
            message = f"{message} Details: {errors}"
        super().__init__(message)
    pass


class AuthenticationError(Exception):
    """Raised when authentication fails"""

    def __init__(self, message="Authentication failed."):
        super().__init__(message)
    pass


class AuthorizationError(Exception):
    """Raised when user is not authorized to perform an action"""
    def __init__(self, message="User is not authorized to perform this action."):
        super().__init__(message)
    pass


class EventNotFoundError(Exception):
    """Raised when an event is not found"""
    def __init__(self, event_id=None, message=None):
        if message is None:
            if event_id is not None:
                message = f"Event with id '{event_id}' was not found."
            else:
                message = "Event was not found."
        super().__init__(message)
    pass


class NotificationNotFoundError(Exception):
    """Raised when a notification is not found"""
    def __init__(self, notification_id=None, message=None):
        if message is None:
            if notification_id is not None:
                message = f"Notification with id '{notification_id}' was not found."
            else:
                message = "Notification was not found."
        super().__init__(message)
    pass 