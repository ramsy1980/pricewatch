from src.models import Payment
from datetime import datetime


def test_new_payment():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    payment_id = "payment_id"
    user_id = "user_id"
    amount = 1
    created = datetime.utcnow()

    payment = Payment(payment_id, user_id, amount, created)

    assert payment.payment_id == payment_id
    assert payment.user_id == user_id
    assert payment.amount == amount
    assert payment.created == created
