from abc import ABC, abstractmethod


class Promotion(ABC):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not new_name:
            raise ValueError("Provide a name for the discount.")

        if not isinstance(new_name, str):
            raise TypeError("Provide the new name as a string.")

        self._name = new_name

    @abstractmethod
    def apply_promotion(self, price: int | float, quantity: int | float) -> int | float:
        pass


class NoPromotion(Promotion):
    def apply_promotion(self, price, quantity):
        return price * quantity


class PromotionDiscountPercent(Promotion):
    def __init__(self, name: str, percent: int):
        """
        Initializes the Discount-Percent class.
        :param percent: The percent as whole value. For 20% insert 20.
        """
        super().__init__(name)

        if not isinstance(percent, int):
            raise TypeError("Please provide an int value.")

        if not 0 < percent <= 100:
            raise ValueError("Please provide a percent value between 0 and 100.")

        self._percent = (100 - percent) / 100

    def apply_promotion(self, price, quantity):
        return price * quantity * self._percent


class PromotionEveryXFree(Promotion):
    def __init__(self, name: str, x: int, percent=100):
        super().__init__(name)

        if not isinstance(x, int):
            raise TypeError("Please provide an integer.")

        if not x > 1:
            raise ValueError("Please provide a number > 1.")

        self._x = x
        self._percent = percent / 100

    def apply_promotion(self, price, quantity):
        bill = quantity * price
        promotion = (quantity // self._x) * price * self._percent

        return bill - promotion
