"""
store module

This module provides a `Store` class to manage a collection of product instances. It includes methods to handle product inventory, manage a shopping cart, and process orders. The module ensures thread safety using locks.

Classes:
    Store

Class Store:
    Represents a store containing product instances.

    Methods:
        __init__(self, products: list[Product]):
            Initializes a new Store instance with a list of products.

        __len__(self):
            Returns the number of products in the store.

        get_shopping_cart(self) -> ShoppingList:
            Returns the shopping cart of the store.

        add_product(self, product: Product) -> str:
            Adds a product to the store. The product must be of type Product.

        remove_product(self, product) -> str:
            Removes a given product from the store.

        get_total_quantity(self) -> int:
            Returns the total quantity of all items in the store.

        get_all_products(self):
            Returns all products in the store.

        get_all_active_products(self) -> list[Product]:
            Returns all active products in the store.

        get_all_available_products(self) -> list[Product]:
            Returns all items in stock in the store.

        show_all_products(self):
            Prints an unrestricted list of all products in the store.

        start_order(self) -> None:
            Prompts the user for a shopping list by listing all available products and prompting the quantity the user wants to acquire.

        _order(self) -> float:
            Removes the shopping-list item's quantities and returns the total price.

        _finalize_order(self) -> None:
            Finishes the order by printing the bill and the amount of items bought and resetting the shopping-cart.
"""

from math import inf, isinf

import prompts
from products import Product
from shoppingcart import ShoppingCart


class Store:
    """
    Creates a store containing Product instances.
    Provide list of products for instantiation.
    """

    __slots__ = ["_products", "_shopping_cart"]

    def __len__(self):
        return sum(
            product.quantity
            if not isinf(product.quantity)
            else 0
            for product in self._products
        )

    def __init__(self, products: list[Product]):
        """ Inits the Store Instance with validity check. """
        if not isinstance(products, list):
            raise ValueError("The products should be of type list.")

        for product in products:
            if not isinstance(product, Product):
                raise ValueError("Store products must be instances of Product")

        self._products = products
        # I'm aware the cart should be connected to the user and not the store, but
        # for this single-user store it's sufficient.
        self._shopping_cart = ShoppingCart()

    @property
    def shopping_cart(self) -> ShoppingCart:
        """
        Returns the Shopping-Cart of the store.
        :return: The Shopping-Cart of the store
        """
        return self._shopping_cart

    @property
    def products(self):
        return self._products

    def add_product(self, product: Product) -> str:
        """ Adds a product to the store. Must be of type Product. """
        if isinstance(product, Product):
            self._products.append(product)
            return product.name

        raise ValueError("Store products must be instances of Product")

    def remove_product(self, product) -> str:
        """ Removes given Product from Store """
        if not isinstance(product, Product):
            raise ValueError("Store products must be instances of Product")

        if any(p == product for p in self._products):
            self._products.remove(product)

        return product.name

    def get_all_products(self):
        """ Return all products """
        return self._products

    def get_all_active_products(self) -> list[Product]:
        """ Return all active products """
        return list(filter(
            lambda p: p.is_active(),
            self.get_all_products()
        ))

    def get_all_available_products(self) -> list[Product]:
        """ Return all items in stock """
        return list(filter(
            self._product_in_stock,
            self.get_all_active_products()
        ))

    def _product_in_stock(self, product: Product):
        return product.quantity > 0

    def get_all_available_products_for_current_cart(self):
        return list(filter(
            lambda item: self.shopping_cart[item.name] <= item.maximum
            if hasattr(item, "maximum")
            else inf,
            self.get_all_available_products()
        ))

    def show_all_products(self) -> None:
        """
        Prints an unrestricted list of all products
        """
        product_infos = [
            product.show()
            for product in self.get_all_products()
        ]

        for idx, product_info in enumerate(product_infos):
            print(f"{idx + 1}. {product_info}")

    def start_order(self) -> None:
        """
        Prompts the user for a shopping list by listing all available
        products and prompting the quantity the user wants to acquire.
        """

        # Guard clause for empty shop
        if len(self.get_all_available_products_for_current_cart()) == 0:
            print("Currently all items are out of stock.")
            return

        # Prompt which products the user wants to acquire
        while True:
            order_item = prompts.prompt_order_item(self)

            # guard clause to exit shopping and charge the user
            if order_item is None:
                return self._finalize_order()

            quantity = prompts.prompt_order_item_quantity(order_item)

            # guard clause to exit shopping and charge the user
            if quantity is None:
                return self._finalize_order()

            available_stock = order_item.quantity - self.shopping_cart[order_item.name]

            if available_stock >= quantity:
                self.shopping_cart.add_item(order_item, quantity)

            else:
                print(f"Only {available_stock} items are in stock.", end="\n\n")

            # Print the current shopping-list-state.
            print(
                "_____________",
                "\nShopping-Cart contains:"
            )
            for name, quantity in self.shopping_cart.cart.items():
                print(f"{name}: {quantity}")

            print(
                "_____________",
                "\n\nWhat else do you want to buy?"
            )

    def _order(self) -> float:
        """ Removes the shopping-list item's quantities and returns the total price. """
        bill = 0
        cart = self.shopping_cart.cart

        for product_name, quantity in cart.items():

            product = next(
                (p for p in self._products if p.name == product_name)
            )

            try:
                # first check if product is in stock
                product.buy(quantity)

                # update bill if it's available
                bill += product.discount.apply_promotion(
                    price=product.price,
                    quantity=quantity
                )
            except ValueError:
                print(f"{product.name} is out of stock.")

        return bill

    def _finalize_order(self) -> None:
        """
        Finishes the order by printing the bill and the amount of items bought
        and resetting the shopping-cart.
        """
        bill = self._order()

        amount_products = sum(
            quantity for quantity in self._shopping_cart.cart.values()
        )

        # Reset the cart
        self._shopping_cart.clear()

        print("********")
        print(f"Order made! Total payment: ${bill} for {amount_products} products.")
