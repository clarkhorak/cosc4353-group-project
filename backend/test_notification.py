from datetime import datetime
from app.models.notification import NotificationCreate, NotificationType
from app.services.notification_service import NotificationService
import asyncio

def test_notification_service():
    print("🧪 Testing NotificationService...")
    service = NotificationService()
    # Create notification
    create_data = NotificationCreate(
        user_id="1",
        type=NotificationType.EVENT_ASSIGNMENT,
        title="Assigned to Event",
        message="You have been assigned to the Community Cleanup event",
        event_id="1"
    )
    notification = asyncio.run(service.create_notification(create_data))
    assert notification.id == 1
    print("  ✅ Notification created:", notification)
    # List notifications for user
    notifications = asyncio.run(service.list_notifications_for_user("1"))
    assert len(notifications) == 1
    print("  ✅ List notifications for user passed")
    # Mark as read
    updated = asyncio.run(service.mark_as_read(1))
    assert updated.is_read is True
    print("  ✅ Mark as read passed")
    # Delete notification
    deleted = asyncio.run(service.delete_notification(1))
    assert deleted is True
    print("  ✅ Delete notification passed")
    # List after delete
    notifications = asyncio.run(service.list_notifications_for_user("1"))
    assert len(notifications) == 0
    print("  ✅ List after delete passed")
    print("🎉 All NotificationService tests passed!")

if __name__ == "__main__":
    test_notification_service() 