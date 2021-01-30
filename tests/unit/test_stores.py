from src.models import Store


def test_new_store():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    name = "name"
    currency_symbol = "currency_symbol"
    url_prefix = "url_prefix"
    css_selector = "css_selector"
    css_selector_out_of_stock = "css_selector_out_of_stock"

    store = Store(name, currency_symbol, url_prefix, css_selector, css_selector_out_of_stock)

    assert store.name == name
    assert store.currency_symbol == currency_symbol
    assert store.url_prefix == url_prefix
    assert store.css_selector == css_selector
    assert store.css_selector_out_of_stock == css_selector_out_of_stock
