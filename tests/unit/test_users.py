from pricewatch.models.user import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    user = User('John Doe', 'FlaskIsAwesome', 'john.doe@gmail.com')
    assert user.name == 'John Doe'
    assert user.email == 'john.doe@gmail.com'
    assert user.password == 'FlaskIsAwesome'
