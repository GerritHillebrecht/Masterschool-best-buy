import pytest
from products import Product


def test_masterschool_default_test():
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    assert bose.buy(50) == 12500
    assert mac.buy(100) == 145000
    assert mac.is_active() is True


pytest.main()
