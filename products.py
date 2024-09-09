"""
products module

This module provides a `Product` class to represent store products with
attributes such as name, price, quantity, and active status. It includes
methods to manage product stock, activation status, and purchase operations.
The module ensures thread safety using locks.

Classes:
    Product

Functions:
    _check_initialization(name, price, quantity, active)

Class Product:
    Represents a store product with attributes name, price, quantity, and active status.

    Methods:
        __init__(self, name: str, price: int | float, quantity: int, active=True):
            Initializes a new product instance with the given attributes.

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
            Processes a purchase of the specified quantity, updates stock,
            and returns the total price.

Function _check_initialization:
    Validates the initialization arguments for the Product class.
"""
from threading import Lock


class Product:
    """
    Represents a store-product. Requires name, price and quantity.
    Will be initialized as active.
    """

    def __init__(
            self,
            name: str,
            price: int | float,
            quantity: int,
            active=True
    ):
        """ Checks the validity of inputs and sets instance attributes. """
        # Assert correct inputs
        _check_initialization(name, price, quantity, active)

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = active
        self.lock = Lock()

    def get_quantity(self) -> float:
        """ Returns the current stock. """
        return self.quantity

    def set_quantity(self, quantity):
        """ Updates the current stock. """
        # Lock the resource for parallel threads while handling.
        with self.lock:
            self.quantity = quantity

            if quantity == 0:
                self.deactivate()
                return

            if not self.is_active():
                self.activate()

    def is_active(self) -> bool:
        """ Returns whether the product is shown in the store. """
        return self.active

    def activate(self):
        """ Activates the product for the store. """
        # Lock the resource for parallel threads while handling.
        with self.lock:
            self.active = True

    def deactivate(self):
        """ Deactivates the product for the store. """
        # Lock the resource for parallel threads while handling.
        with self.lock:
            self.active = False

    def show(self) -> str:
        """ Returns a printable string of all product information. """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity) -> float:
        """
        Updates the stock and return the price of the order.
        Throws an error if out of stock.
        """

        # Lock the resource for parallel threads while handling.
        with self.lock:
            if self.quantity >= quantity:
                self.quantity -= quantity

                if self.quantity == 0:
                    self.deactivate()

                return quantity * self.price

            raise ValueError(
                f"Stock of {self.name} is insufficient ({self.quantity}) to buy {quantity}."
            )


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
    if not isinstance(quantity, int):
        raise TypeError("The quantity should be a whole number as int.")
    if not quantity >= 0:
        raise ValueError("The quantity cannot be negative.")

    # active
    if not isinstance(active, bool):
        raise TypeError("Active should be represented as a boolean value.")
