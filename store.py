from threading import Lock
from products import Product


class Store:
    """
    Creates a store containing Product instances.
    Provide list of products for instantiation.
    """

    def __init__(self, products: list):
        """ Inits the Store Instance with validity check. """
        if not isinstance(products, list):
            raise ValueError("The products should be of type list.")

        for product in products:
            if not isinstance(product, Product):
                raise ValueError("Store products must be instances of Product")

        self.products = products
        self.lock = Lock()

    def add_product(self, product: Product) -> str:
        """ Adds a product to the store. Must be of type Product. """
        if isinstance(product, Product):
            with self.lock:
                self.products.append(product)
            return product.name

        raise ValueError("Store products must be instances of Product")

    def remove_product(self, product) -> str:
        """ Removes given Product from Store """
        if not isinstance(product, Product):
            raise ValueError("Store products must be instances of Product")

        with self.lock:
            if any(p == product for p in self.products):
                self.products.remove(product)

        return product.name

    def get_total_quantity(self) -> int:
        """ Returns the stock of all items in the store. """
        return sum(product.quantity for product in self.products)

    def get_all_products(self) -> list[Product]:
        """ Return all active products """
        return list(filter(lambda p: p.active, self.products))

    def order(self, shopping_list: list[tuple]) -> float:
        """ Removes the shopping-list items quantities and return the total price. """
        if not isinstance(shopping_list, list):
            raise ValueError("The shopping-list must of type - wait for it - list.")

        for item in shopping_list:
            if not isinstance(item[0], Product) or not isinstance(item[1], (float, int)):
                raise ValueError("Provide a Product and the quantity as int / float.")

        with self.lock:
            bill = 0

            for item in shopping_list:
                product, quantity = item

                try:
                    product.buy(quantity)
                    bill += product.price * quantity
                except ValueError:
                    print(f"{product.name} is out of stock.")
                    product.deactivate()

        return bill
