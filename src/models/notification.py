from dataclasses import dataclass, field
from typing import Dict
from src.models.model import Model
from src.models.user import User
from datetime import datetime
from enum import Enum
import src.models.alert


class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"

    def __str__(self):
        return str(self.value)


@dataclass(eq=False)
class Notification(Model):
    _id: str
    user_id: str
    alert_id: str
    notification_type: NotificationType
    created: datetime
    collection: str = field(init=False, default="notifications")

    def __post_init__(self):
        self.user = User.get_by_id(self.user_id)
        self.alert = src.models.alert.Alert.get_by_id(self.alert_id)

    def __repr__(self) -> str:
        return f"<Notification user_id={self.user_id}>"

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "alert_id": self.alert_id,
            "notification_type": self.notification_type.value,
            "created": self.created
        }
