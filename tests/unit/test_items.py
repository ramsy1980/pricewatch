from src.models import Item


def test_new_item():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    url = "url"
    store_id = "store_id"
    price = 1.0
    out_of_stock = False
    item = Item(url, store_id, price, out_of_stock)

    assert item.url == url
    assert item.store_id == store_id
    assert item.price == price
    assert item.out_of_stock == out_of_stock
