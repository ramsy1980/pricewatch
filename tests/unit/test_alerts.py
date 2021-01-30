from src.models import Alert


def test_new_alert():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    name = "name"
    item_id = "item_id"
    price_limit = 1.0
    user_email = "user@email.tld"

    alert = Alert(name, item_id, price_limit, user_email)

    assert alert.name == name
    assert alert.item_id == item_id
    assert alert.price_limit == price_limit
    assert alert.user_email == user_email
