from uuid import uuid4
from dataclasses import dataclass, field
from typing import Dict
from models.model import Model
from common.utils import Utils
import models.user.errors as errors


@dataclass
class User(Model):
    collection: str = field(init=False, default='users')
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid4().hex)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        try:
            return cls.find_one_by('email', email)
        except TypeError:
            raise errors.UserNotFoundError('A user with this email does not exist')

    @classmethod
    def register(cls, email: str, password: str) -> bool:
        if not Utils.email_is_valid(email):
            raise errors.InvalidEmailError('This email does not have the right format')
        try:
            cls.find_by_email(email)
            raise errors.UserAlreadyRegisteredError('This email is already linked to an existing account.')
        except errors.UserNotFoundError:
            User(email, Utils.hash_password(password)).save_to_db()

        return True
