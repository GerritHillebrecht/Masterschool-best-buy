"""
products module

This module provides a `Product` class to represent store products with attributes such as name, price, quantity, and active status. It includes methods to manage product stock, activation status, and purchase operations. The module ensures thread safety using locks.

Classes:
    Product

Functions:
    _check_initialization(name, price, quantity, active)

Class Product:
    Represents a store product with attributes name, price, quantity, and active status.

    Methods:
        __init__(self, name: str, price: int | float, quantity: int, active=True):
            Initializes a new product instance with the given attributes.

        get_name(self):
            Returns the name of the product.

        get_price(self):
            Returns the price of the product.

        get_quantity(self) -> float:
            Returns the current stock quantity of the product.

        set_quantity(self, quantity):
            Updates the stock quantity of the product and adjusts its active status.

        is_active(self) -> bool:
            Returns whether the product is active in the store.

        activate(self):
            Activates the product for sale in the store.

        deactivate(self):
            Deactivates the product, making it unavailable for sale.

        show(self) -> str:
            Returns a string representation of the product's information.

        buy(self, quantity) -> float:
            Processes a purchase of the specified quantity, updates stock, and returns the total price.

Function _check_initialization:
    Validates the initialization arguments for the Product class.
"""
from math import inf
from promotion import Promotion, NoPromotion


class Product:
    """
    Represents a store-product. Requires name, price and quantity.
    Will be initialized as active.
    """

    __slots__ = ["_name", "_price", "_quantity", "_promotion", "_active"]

    def __init__(
            self,
            name: str,
            price: int | float,
            quantity: int | float,
            promotion: Promotion = NoPromotion("No Promotion"),
            active=True
    ):
        """ Checks the validity of inputs and sets instance attributes. """
        # Assert correct inputs
        _check_initialization(name, price, quantity, active)

        self._name = name
        self._price = price
        self._quantity = quantity
        self._promotion = promotion
        self._active = active

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not new_name:
            raise ValueError("Please provide a name")

        if not isinstance(new_name, str):
            raise TypeError("Please provide a str.")

        self._name = new_name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if not isinstance(new_price, (int, float)):
            raise TypeError("Please provide the new price as an int or float.")

        if not new_price >= 0:
            raise ValueError("Please provide a price larger than or equal to 0.")

        self._price = new_price

    @property
    def quantity(self) -> float:
        """ Returns the current stock. """
        return self._quantity

    @quantity.setter
    def quantity(self, new_quantity):
        if not isinstance(new_quantity, int):
            raise TypeError("Please provide the new quantity as an int.")

        if not new_quantity >= 0:
            raise ValueError("Please provide a quantity of at least 0.")

        self._quantity = new_quantity

        if new_quantity == 0:
            self.deactivate()
            return

        if not self.is_active():
            self.activate()

    @property
    def discount(self):
        return self._promotion

    def is_active(self) -> bool:
        """ Returns whether the product is shown in the store. """
        return self._active

    def activate(self):
        """ Activates the product for the store. """
        self._active = True

    def deactivate(self):
        """ Deactivates the product for the store. """
        self._active = False

    def show(self) -> str:
        """ Returns a printable string of all product information. """
        return f"{self._name}, Price: {self._price}, Quantity: {self.quantity}, Promotion: {self._promotion.name}"

    def buy(self, quantity) -> float:
        """
        Updates the stock and return the price of the order.
        Throws an error if out of stock.
        """

        if self._quantity >= quantity:
            self._quantity -= quantity

            if self._quantity == 0:
                self.deactivate()

            return quantity * self._price

        raise ValueError(
            f"Stock of {self._name} is insufficient ({self._quantity}) to buy {quantity}."
        )

    def set_promotion(self, promotion):
        if not isinstance(promotion, Promotion):
            raise TypeError("The promotion should be of type Promotion or descendant child")

        self._promotion = promotion


class NonStockedProduct(Product):
    def __init__(
            self,
            name: str,
            price: int | float,
            promotion: Promotion = NoPromotion("No Promotion"),
            active=True
    ):
        super().__init__(
            name=name,
            price=price,
            quantity=inf,
            active=active,
            promotion=promotion
        )

    def show(self) -> str:
        """ Returns a printable string of all product information. """
        return f"{self._name}, Price: {self._price}, Quantity: Unlimited, Promotion: {self._promotion.name}"


class LimitedProduct(Product):
    __slots__ = ["_maximum"]

    def __init__(
            self,
            name: str,
            price: int | float,
            maximum: int,
            promotion: Promotion = NoPromotion("No Promotion"),
            quantity=inf,
            active=True,
    ):
        super().__init__(
            name=name,
            price=price,
            quantity=quantity,
            active=active,
            promotion=promotion,
        )

        self._check_and_set_maximum_value(maximum)

    @property
    def maximum(self):
        return self._maximum

    @maximum.setter
    def maximum(self, new_maximum):
        self._check_and_set_maximum_value(new_maximum)

    def show(self):
        """ Returns a printable string of all product information. """
        return f"{self._name}, Price: {self._price}, Promotion: {self._promotion.name}, limited to {self.maximum} per order!"

    def _check_and_set_maximum_value(self, maximum):
        if not isinstance(maximum, int):
            raise TypeError("maximum should be of type int.")

        if maximum < 1:
            raise ValueError("The maximum value should be at least 1.")

        self._maximum = maximum


def _check_initialization(name, price, quantity, active):
    """
    Checks the validity of the __init__ arguments.
    """
    # name
    if not isinstance(name, str):
        raise TypeError("The product-name should of type string.")
    if not len(name) > 0:
        raise ValueError("The product-name should not be empty.")

    # price
    if not isinstance(price, (int, float)):
        raise TypeError("The price should be of type int or float.")
    if not price >= 0:
        raise ValueError("The price should be a positive number.")

    # quantity
    if not isinstance(quantity, (int, float)):
        raise TypeError("The quantity should be a whole number as int or infinity.")
    if not quantity >= 0:
        raise ValueError("The quantity cannot be negative.")

    # active
    if not isinstance(active, bool):
        raise TypeError("Active should be represented as a boolean value.")
