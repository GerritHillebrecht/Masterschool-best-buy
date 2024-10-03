"""
products module

This module provides a `Product` class to represent store products with attributes such as name, price, quantity, and active status. It includes methods to manage product stock, activation status, and purchase operations. Additionally, it includes specialized product classes for non-stocked and limited products.

Classes:
    Product
    NonStockedProduct
    LimitedProduct

Functions:
    _check_initialization(name, price, quantity, active)

Class Product:
    Represents a store product with attributes name, price, quantity, and active status.

    Methods:
        __init__(self, name: str, price: int | float, quantity: int | float, promotion: Promotion = NoPromotion("No Promotion"), active=True):
            Initializes a new product instance with the given attributes.

        __str__(self):
            Returns a printable string of all product information.

        __gt__(self, other) -> bool:
            Compares the price with a different product instance.

        __ge__(self, other):
            Compares the price with a different product instance.

        __lt__(self, other):
            Compares the price with a different product instance.

        __le__(self, other):
            Compares the price with a different product instance.

        name(self):
            Returns the private property name.

        name(self, new_name):
            Sets the private property name.

        price(self):
            Returns the private property price.

        price(self, new_price):
            Sets the private property price.

        quantity(self) -> float:
            Returns the current stock.

        quantity(self, new_quantity):
            Sets the current stock.

        promotion(self):
            Returns the private property promotion.

        is_active(self) -> bool:
            Returns whether the product is shown in the store.

        activate(self):
            Activates the product for the store.

        deactivate(self):
            Deactivates the product for the store.

        buy(self, quantity) -> float:
            Updates the stock and returns the price of the order.

        set_promotion(self, promotion):
            Sets a product promotion of type Promotion.

Class NonStockedProduct:
    Represents a store product with unlimited quantity.

    Methods:
        __init__(self, name: str, price: int | float, promotion: Promotion = NoPromotion("No Promotion"), active=True):
            Initializes a new non-stocked product instance with the given attributes.

        __str__(self):
            Returns a printable string of all product information.

Class LimitedProduct:
    Represents a store product with a maximum limit.

    Methods:
        __init__(self, name: str, price: int | float, maximum: int, promotion: Promotion = NoPromotion("No Promotion"), quantity=inf, active=True):
            Initializes a new limited product instance with the given attributes.

        __str__(self):
            Returns a printable string of all product information.

        maximum(self):
            Returns the private property maximum.

        maximum(self, new_maximum):
            Sets the private property maximum.

        _check_and_set_maximum_value(self, maximum):
            Avoids repeated code, checks the type and value of maximum and sets it.

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

    # Memory + speed optimization
    __slots__ = ("_name", "_price", "_quantity", "_promotion", "_active")

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

    def __str__(self):
        """ Returns a printable string of all product information. """
        name = self._name
        price = f"Price: {self._price}"
        quantity = f"Quantity: {self.quantity}"
        promotion = f"Promotion: {self._promotion.name}"

        return f"{name}, {price}, {quantity}, {promotion}"

    def __gt__(self, other) -> bool:
        """
        Compares the price with a different product instance.
        :param other: The other product instance. Must be of type Product or descendant.
        """
        if not isinstance(other, Product):
            raise TypeError("Please provide a product of type Product.")

        return self.price > other.price

    def __ge__(self, other):
        """
        Compares the price with a different product instance.
        :param other: The other product instance. Must be of type Product or descendant.
        """
        if not isinstance(other, Product):
            raise TypeError("Please provide a product of type Product.")

        return self.price >= other.price

    def __lt__(self, other):
        """
        Compares the price with a different product instance.
        :param other: The other product instance. Must be of type Product or descendant.
        """
        if not isinstance(other, Product):
            raise TypeError("Please provide a product of type Product.")

        return self.price < other.price

    def __le__(self, other):
        """
        Compares the price with a different product instance.
        :param other: The other product instance. Must be of type Product or descendant.
        """
        if not isinstance(other, Product):
            raise TypeError("Please provide a product of type Product.")

        return self.price <= other.price

    @property
    def name(self):
        """ Returns the private property name. """
        return self._name

    @name.setter
    def name(self, new_name):
        """ Sets the private property name. """
        if not new_name:
            raise ValueError("Please provide a name")

        if not isinstance(new_name, str):
            raise TypeError("Please provide a str.")

        self._name = new_name

    @property
    def price(self):
        """ Returns the private property price. """
        return self._price

    @price.setter
    def price(self, new_price):
        """ Sets the private property name. """
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
        """ Sets the current stock """
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
    def promotion(self):
        """ Returns the private property prmotion. """
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
        """ Sets a product-Promotion of type Promotion. """
        if not isinstance(promotion, Promotion):
            raise TypeError("The promotion should be of type Promotion or descendant child")

        self._promotion = promotion


class NonStockedProduct(Product):
    """
    Represents a store-product with unlimited quantity. Requires name, price and quantity.
    Will be initialized as active.
    """

    def __init__(
            self,
            name: str,
            price: int | float,
            promotion: Promotion = NoPromotion("No Promotion"),
            active=True
    ):
        """ Calls the Base class init-function and sets quantity to infinity. """
        super().__init__(
            name=name,
            price=price,
            quantity=inf,
            active=active,
            promotion=promotion
        )

    def __str__(self):
        """ Returns a printable string of all product information. """
        name = self._name
        price = f"Price: {self._price}"
        quantity = "Quantity: Unlimited"
        promotion = f"Promotion: {self._promotion.name}"

        return f"{name}, {price}, {quantity}, {promotion}"


class LimitedProduct(Product):
    """
    Represents a store-product with a maximum limit.
    Requires name, price, quantity and maximum. Will be initialized as active.
    """
    # Adds slot for extra property
    __slots__ = "_maximum"

    def __init__(
            self,
            name: str,
            price: int | float,
            maximum: int,
            promotion: Promotion = NoPromotion("No Promotion"),
            quantity=inf,
            active=True,
    ):
        """ Calls the Base class init-function """
        super().__init__(
            name=name,
            price=price,
            quantity=quantity,
            active=active,
            promotion=promotion,
        )

        self._check_and_set_maximum_value(maximum)

    def __str__(self):
        """ Returns a printable string of all product information. """
        name = self.name
        price = f"Price: {self._price}"
        promotion = f"Promotion: {self._promotion.name}"
        maximum = f"limited to {self.maximum} per order!"

        return f"{name}, {price}, {promotion}, {maximum}"

    @property
    def maximum(self):
        """ Returns the private property maximum. """
        return self._maximum

    @maximum.setter
    def maximum(self, new_maximum):
        """ Sets the private property maximum. """
        self._check_and_set_maximum_value(new_maximum)

    def _check_and_set_maximum_value(self, maximum):
        """ Avoids repeated code, checks the type and value of maximum and sets it """
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
