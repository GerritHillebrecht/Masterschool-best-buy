"""
shoppingCart module

This module provides a `ShoppingCart` class to manage the items in a shopping cart.
It includes methods to add items, clear the cart,
and retrieve information about the items in the cart.

Classes:
    ShoppingCart

Class ShoppingCart:
    Represents a shopping cart that holds products and their quantities.

    Methods:
        __init__(self):
            Initializes the Shopping-Cart class instance.

        __str__(self) -> str:
            Returns the dictionary representing the cart as a string.

        __len__(self) -> int:
            Gets the number of different items in the shopping cart.

        __getitem__(self, product_name: str) -> int | float:
            Gets the quantity of a specific product in the shopping cart.

        cart(self):
            Returns the private property _cart.

        add_item(self, product: Product, quantity: int | float) -> None:
            Adds an item to the shopping cart.

        clear(self) -> None:
            Clears the shopping cart.
"""

from products import Product


class ShoppingCart:
    __slots__ = ["_cart"]

    def __init__(self):
        """ Initializes the Shopping-Cart class-instance. """
        self._cart = {}
        pass

    def __str__(self) -> str:
        """
        Returns the dictionary representing the cart as str.
        """
        return str(self._cart)

    def __len__(self) -> int:
        """
        Gets the amount of items in the shopping cart.
        Example: There's a Macbook and an Apple Pen in the cart, this will return 2,
        ignoring the amount of each product in the bag.
        :return: Number of items in the cart.
        """
        return len(self._cart)

    def __getitem__(self, product_name: str) -> int | float:
        """
        Gets the amount of a product in the shopping cart.
        :param product_name: The name of the product you want to get the amount of.
        :return: The amount of product. Returns zero if not in the list
        """
        if not isinstance(product_name, str):
            raise TypeError("Product-name needed to fetch quantity.")

        return self._cart.get(product_name, 0)

    @property
    def cart(self):
        return self._cart

    def add_item(self, product: Product, quantity: int | float) -> None:
        """ Adds an item to the shopping-cart. """

        if not isinstance(product, Product):
            print("Provide a product to add to the shopping-cart.")
            return

        if not isinstance(quantity, (int, float)):
            print("Provide a valid quantity to add to the shopping-cart.")
            return

        updated_cart_value = self._cart.get(product.name, 0) + quantity

        if hasattr(product, "maximum"):
            if quantity > product.maximum:
                print(f"You can only have {product.maximum} of {product.name}")
                return

            if updated_cart_value > product.maximum:
                print(f"The maximum of {product.name} has been reached.")
                return

        self._cart[product.name] = updated_cart_value

    def clear(self) -> None:
        """ Clears the shopping-cart. """
        self._cart = {}
