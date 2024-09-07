from threading import Lock


class Product:
    def __init__(self, name, price, quantity, active=True):
        # Assert correct inputs
        _check_initialization(name, price, quantity, active)

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = active
        self.lock = Lock()

    def get_quantity(self) -> float:
        return self.quantity

    def set_quantity(self, quantity):
        # Lock the resource for parallel threads while handling.
        with self.lock:
            self.quantity = quantity

    def is_active(self) -> bool:
        return self.active

    def activate(self):
        # Lock the resource for parallel threads while handling.
        with self.lock:
            self.active = True

    def deactivate(self):
        # Lock the resource for parallel threads while handling.
        with self.lock:
            self.active = False

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity) -> float:
        # Lock the resource for parallel threads while handling.
        with self.lock:
            if self.quantity >= quantity:
                self.quantity -= quantity
                return quantity * self.price

            raise ValueError(
                f"Stock of {self.name} is insufficient ({self.quantity}) to buy {quantity}."
            )


def _check_initialization(name, price, quantity, active):
    """
    Checks the validity of the __init__ arguments.
    """
    # name
    if not type(name) is str:
        raise TypeError("The product-name should of type string.")
    if not len(name) > 0:
        raise ValueError("The product-name should not be empty.")

    # price
    if not (type(price) is int or type(price) is float):
        raise TypeError("The price should be of type int or float.")
    if not price >= 0:
        raise ValueError("The price should be a positive number.")

    # quantity
    if not type(quantity) is int:
        raise TypeError("The quantity should be a whole number as int.")
    if not quantity >= 0:
        raise ValueError("The quantity cannot be negative.")

    # active
    if not type(active) is bool:
        raise TypeError("Active should be represented as a boolean value.")
