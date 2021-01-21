from uuid import uuid4
from dataclasses import dataclass, field
from typing import Dict
from models.model import Model
from common.utils import Utils
import models.user.errors as errors


@dataclass
class User(Model):
    name: str
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid4().hex)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

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
