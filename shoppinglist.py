from products import Product


class ShoppingList:
    __slots__ = ["_cart"]

    def __init__(self):
        """ Initializes the Shopping-Cart class-instance. """
        self._cart = {}
        pass

    def __str__(self):
        return str(self._cart)

    def __len__(self):
        return len(self._cart)

    def get_cart(self):
        return self._cart

    def add_item(self, product: Product, quantity: int | float) -> None:
        """ Adds an item to the shopping-cart. """

        if not isinstance(product, Product):
            print("Provide a product to add to the shopping-cart.")
            return

        if not isinstance(quantity, (int, float)):
            print("Provide a valid quantity to add to the shopping-cart.")
            return

        self._cart[product.get_name()] = self._cart.get(product.get_name(), 0) + quantity

    def get_item_quantity(self, product: Product) -> int:
        """ Returns the quantity of a product in the shopping-cart. """

        if not isinstance(product, Product):
            print("Provide a product to add to the shopping-cart.")
            return 0

        return self._cart.get(product.get_name(), 0)

    def clear_cart(self) -> None:
        """ Clears the shopping-cart. """

        self._cart = {}


from products import Product


class ShoppingList:
    __slots__ = ["_cart"]

    def __init__(self):
        """ Initializes the Shopping-Cart class-instance. """
        self._cart = {}
        pass

    def __str__(self):
        return str(self._cart)

    def __len__(self):
        return len(self._cart)

    def get_cart(self):
        return self._cart

    def add_item(self, product: Product, quantity: int | float) -> None:
        """ Adds an item to the shopping-cart. """

        if not isinstance(product, Product):
            print("Provide a product to add to the shopping-cart.")
            return

        if not isinstance(quantity, (int, float)):
            print("Provide a valid quantity to add to the shopping-cart.")
            return

        self._cart[product.get_name()] = self._cart.get(product.get_name(), 0) + quantity

    def get_item_quantity(self, product: Product) -> int:
        """ Returns the quantity of a product in the shopping-cart. """

        if not isinstance(product, Product):
            print("Provide a product to add to the shopping-cart.")
            return 0

        return self._cart.get(product.get_name(), 0)

    def clear_cart(self) -> None:
        """ Clears the shopping-cart. """

        self._cart = {}
