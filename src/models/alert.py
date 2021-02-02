from flask import current_app
from uuid import uuid4
from dataclasses import dataclass, field
from typing import Dict
from datetime import datetime, timedelta
from src.models.item import Item
from src.models.model import Model
from src.models.user import User
from src.models.notification import Notification, NotificationType
from src.libs.sendgrid import SendGrid
from src.libs.twilio import Twilio


@dataclass(eq=False)
class Alert(Model):

    collection: str = field(init=False, default='alerts')
    name: str
    item_id: str
    price_limit: float
    user_email: str
    last_email_sent_at: datetime = None
    last_sms_sent_at: datetime = None

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
            "user_email": self.user_email,
            "last_email_sent_at": self.last_email_sent_at,
            "last_sms_sent_at": self.last_sms_sent_at
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def send_email(self, text_content: str, html_content: str):
        if self.last_email_sent_at and not (datetime.utcnow() > self.last_email_sent_at + timedelta(days=1)):
            print(f"Not sending email. Last email sent at {self.last_sms_sent_at}")
            return

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
        self.last_email_sent_at = datetime.utcnow()
        self.save_to_db()

    def sens_sms(self, text_content: str):
        if not self.user.has_credits():
            print("Insufficient credits. Unable to send SMS.")
            return
        if self.last_sms_sent_at and not (datetime.utcnow() > self.last_sms_sent_at + timedelta(days=1)):
            print(f"Not sending sms. Last sms sent at {self.last_sms_sent_at}")
            return

        date, message_id = Twilio.send_sms(self.user.phone_number, text_content)
        Notification(
            _id=message_id,
            user_id=self.user.id,
            alert_id=self._id,
            notification_type=NotificationType.SMS,
            created=date
        ).save_to_db()
        self.user.consume_one_credit()
        self.last_sms_sent_at = datetime.utcnow()
        self.save_to_db()

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached price under {self.price_limit}. Latest price: {self.item.price}")

            link = f"{current_app.config.get('APP_DOMAIN_URL')}/links/{self.item._id}"

            html_content = f"<p>Your alert {self.name} has reached a price under {self.item.store.currency_symbol} {self.price_limit}.</p> \
                                   <p>The latest price is {self.item.store.currency_symbol} {self.item.price}.</p> \
                                   <p>Go to this address to check your item: <a href='{link}'>{self.name}</a>.\
                                   </p>"
            text_content = f"Your alert {self.name} has reached a price under {self.item.store.currency_symbol} {self.price_limit}. \
                                   The latest price is {self.item.store.currency_symbol} {self.item.price}. \
                                   Go to this address to check your item: {link}."

            if self.user.is_email_verified():
                try:
                    self.send_email(text_content, html_content)
                except Exception as e:
                    excepName = type(e).__name__
                    print(excepName, "Failed to send email", e)

            else:
                print("Unable to send email. Email is not verified.")

            if self.user.is_phone_number_verified():
                try:
                    self.sens_sms(text_content)
                except Exception as e:
                    excepName = type(e).__name__
                    print(excepName, "Failed to send SMS", e)
            else:
                print("Unable to send SMS. Phone number is not verified.")
