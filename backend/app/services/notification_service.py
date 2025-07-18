from typing import List, Optional
from datetime import datetime
from app.models.notification import Notification, NotificationCreate, NotificationUpdate, NotificationResponse
from app.utils.exceptions import ValidationError

class NotificationService:
    def __init__(self):
        self.notifications: dict[int, NotificationResponse] = {}
        self.next_id = 1

    async def create_notification(self, data: NotificationCreate) -> NotificationResponse:
        now = datetime.utcnow()
        notification = NotificationResponse(
            id=self.next_id,
            user_id=data.user_id,
            type=data.type,
            title=data.title,
            message=data.message,
            event_id=data.event_id,
            created_at=now,
            is_read=False
        )
        self.notifications[self.next_id] = notification
        self.next_id += 1
        return notification

    async def list_notifications_for_user(self, user_id: str) -> List[NotificationResponse]:
        return [n for n in self.notifications.values() if n.user_id == user_id]

    async def mark_as_read(self, notification_id: int) -> NotificationResponse:
        if notification_id not in self.notifications:
            raise ValidationError(f"Notification {notification_id} not found")
        notification = self.notifications[notification_id]
        notification.is_read = True
        self.notifications[notification_id] = notification
        return notification

    async def delete_notification(self, notification_id: int) -> bool:
        if notification_id not in self.notifications:
            raise ValidationError(f"Notification {notification_id} not found")
        del self.notifications[notification_id]
        return True 