from passlib.hash import pbkdf2_sha512
import re


class Utils:
    @staticmethod
    def email_is_valid(email: str) -> bool:
        print("email_is_valid", email)
        email_address_matcher = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def verify_hashed_password(password: str, hashed_password: str) -> bool:
        return pbkdf2_sha512.verify(password, hashed_password)
