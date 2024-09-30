import pytest
from products import Product


def test_product_creation():
    product = Product(name="Airpods Pro 2", price=249, quantity=200)
    assert isinstance(product, Product) is True


def test_invalid_product():
    with pytest.raises(TypeError) as e_info:
        invalid_product = Product(price=249, quantity=200)
    with pytest.raises(ValueError) as e_info:
        invalid_product = Product(name="", price=249, quantity=200)
    with pytest.raises(ValueError) as e_info:
        invalid_product = Product(name="Airpods Pro 2", price=-249, quantity=200)


def test_product_out_of_stock():
    product = Product(name="Airpods Pro 2", price=249, quantity=200)
    product.buy(200)
    assert product.is_active() is False


def test_product_transaction():
    product = Product(name="Airpods Pro 2", price=249, quantity=200)
    price = product.buy(150)
    assert product.quantity == 50 and price == product.price * 150


def test_buy_out_of_stock():
    product = Product(name="Airpods Pro 2", price=249, quantity=200)
    with pytest.raises(Exception) as e_info:
        product.buy(250)
