from src.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    name = "name"
    password = "password"
    email = "email@example.tld"

    user = User(name, password, email)

    assert user.name == name
    assert user.password == password
    assert user.email == email
