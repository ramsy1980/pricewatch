from dataclasses import dataclass, field
from typing import Dict
from src.models.model import Model
from src.models.user import User
from datetime import datetime


@dataclass(eq=False)
class Payment(Model):
    _id: str
    user_id: str
    amount: int
    created: datetime
    collection: str = field(init=False, default="payments")

    def __post_init__(self):
        self.user = User.get_by_id(self.user_id)

    def __repr__(self) -> str:
        return f"<Payment user_id={self.user_id} credits={self.amount}>"

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "amount": self.amount,
            "created": self.created
        }
