"""
Test-cases from the assignment.
All saved inside the store testing.
"""

import pytest
from products import Product, LimitedProduct
from store import Store

# setup initial stock of inventory
mac = Product("MacBook Air M2", price=1450, quantity=100)
bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
pixel = LimitedProduct("Google Pixel 7", price=500, quantity=250, maximum=1)

best_buy = Store([mac, bose])


def test_product_negative_price():
    with pytest.raises(ValueError):
        mac.price = -100  # Should give error


def test_product_print():
    assert str(mac) == "MacBook Air M2, Price: 1450, Quantity: 100, Promotion: No Promotion"


def test_price_comparison():
    assert mac > bose


def test_mac_in_best_buy():
    assert mac in best_buy


def test_pixel_in_best_buy():
    assert pixel not in best_buy
