from uuid import uuid4
from dataclasses import dataclass, field
from typing import Dict
from models.item import Item
from models.model import Model
from models.user import User
from libs.sendgrid import SendGrid
from libs.twilio import Twilio
from models.notification import Notification, NotificationType


@dataclass(eq=False)
class Alert(Model):

    collection: str = field(init=False, default='alerts')
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "price_limit": self.price_limit,
            "item_id": self.item_id,
            "user_email": self.user_email
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached price under {self.price_limit}. Latest price: {self.item.price}")

            html_content = f"<p>Your alert {self.name} has reached a price under {self.item.store.currency_symbol} {self.price_limit}.</p> \
                                   <p>The latest price is {self.item.store.currency_symbol} {self.item.price}.</p> \
                                   <p>Go to this address to check your item: <a href='{self.item.url}'>{self.item.url}</a>.\
                                   </p>"
            text_content = f"Your alert {self.name} has reached a price under {self.item.store.currency_symbol} {self.price_limit}. \
                                   The latest price is {self.item.store.currency_symbol} {self.item.price}. \
                                   Go to this address to check your item: {self.item.url}."

            if self.user.is_email_verified():
                try:
                    date, message_id = SendGrid.send_email(
                        to_emails=[self.user_email],
                        subject=f"Notification for {self.name}",
                        html_content=html_content,
                        text_content=text_content
                    )
                    Notification(
                        _id=message_id,
                        user_id=self.user.id,
                        alert_id=self._id,
                        notification_type=NotificationType.EMAIL,
                        created=date
                    ).save_to_db()
                except Exception as e:
                    excepName = type(e).__name__
                    print(excepName, "Failed to send email")

            else:
                print("Unable to send email. Email is not verified.")

            if self.user.is_phone_number_verified():
                if not self.user.has_credits():
                    print("Insufficient credits. Unable to send SMS.")
                    return

                try:
                    date, message_id = Twilio.send_sms(self.user.phone_number, text_content)
                    Notification(
                        _id=message_id,
                        user_id=self.user.id,
                        alert_id=self._id,
                        notification_type=NotificationType.SMS,
                        created=date
                    ).save_to_db()
                    self.user.consume_one_credit()
                except Exception as e:
                    excepName = type(e).__name__
                    print(excepName, "Failed to send SMS")
            else:
                print("Unable to send SMS. Phone number is not verified.")
