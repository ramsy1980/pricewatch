from uuid import uuid4
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Dict, Union
from models.model import Model
from common.utils import Utils
import models.user.errors as errors
from libs.sendgrid import SendGrid


@dataclass
class User(Model):
    name: str
    email: str
    password: str

    email_verification_send_at: Union[datetime, None] = None
    email_verified_at: Union[datetime, None] = None
    email_verification_token: Union[str, None] = None
    email_verification_token_expires_at: Union[datetime, None] = None

    _id: str = field(default_factory=lambda: uuid4().hex)
    created_at: datetime = field(init=False, default=datetime.utcnow())
    collection: str = field(init=False, default='users')

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "email_verification_send_at": self.email_verification_send_at,
            "email_verified_at": self.email_verified_at,
            "email_verification_token": self.email_verification_token,
            "email_verification_token_expires_at": self.email_verification_token_expires_at
        }

    def send_email_verification(self) -> None:
        self.email_verification_token = uuid4().hex
        verify_email_link = f"http://localhost:5000/emails/verify/{self.email_verification_token}"

        SendGrid.send_email(
            to_emails=[self.email],
            subject="Please verify your email address",
            text_content=f"Please click on the following link to verify you email address: {verify_email_link}",
            html_content=f"<p>Please click on the following link to verify you email address: \
                           <a href='{verify_email_link}'>{verify_email_link}</a></p>"
        )

        self.email_verification_send_at = datetime.utcnow()
        self.email_verification_token_expires_at = self.email_verification_send_at + timedelta(hours=2)

        self.save_to_db()

    def is_email_verified(self):
        return self.email_verified_at is not None

    def verify_email(self) -> bool:
        if self.email_verified_at is not None:
            raise errors.EmailVerificationTokenError('Email is already verified')

        if datetime.utcnow() > self.email_verification_token_expires_at:
            raise errors.EmailVerificationTokenError('This token is expired.')

        self.email_verified_at = datetime.utcnow()
        self.email_verification_token = None
        self.email_verification_token_expires_at = None
        self.save_to_db()

        return True

    @classmethod
    def find_by_email_verification_token(cls, email_verification_token: str) -> "User":
        try:
            return cls.find_one_by('email_verification_token', email_verification_token)
        except TypeError:
            raise errors.EmailVerificationTokenError('This email address cannot be verified.')

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        try:
            return cls.find_one_by('email', email)
        except TypeError:
            raise errors.UserNotFoundError('This email is not associated with an account.')

    @classmethod
    def register(cls, name: str, email: str, password: str) -> "User":
        if not Utils.email_is_valid(email):
            raise errors.InvalidEmailError('This email does not have the right format')
        try:
            cls.find_by_email(email)
            raise errors.UserAlreadyRegisteredError('This email is already associated with an account.')
        except errors.UserNotFoundError:
            user = User(name, email, Utils.hash_password(password))
            user.save_to_db()

            return user

    @classmethod
    def is_login_valid(cls, email: str, password: str) -> bool:
        user = cls.find_by_email(email)
        if not Utils.verify_hashed_password(password, user.password):
            raise errors.IncorrectPasswordError("Your password was incorrect")

        return True
