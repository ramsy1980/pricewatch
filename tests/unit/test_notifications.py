from src.models import Notification
from datetime import datetime


def test_new_notification():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    notification_id = "notification_id"
    user_id = "user_id"
    alert_id = "alert_id"
    notification_type = "sms"
    created = datetime.utcnow()

    notification = Notification(notification_id, user_id, alert_id, notification_type, created)

    assert notification.notification_id == notification_id
    assert notification.user_id == user_id
    assert notification.alert_id == alert_id
    assert notification.notification_type == notification_type
    assert notification.created == created
