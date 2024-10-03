"""
main module

This module initializes the store with a list of products and starts the store program.
It includes functions to start the program and initialize the store inventory with promotions.

Functions:
    start(store: Store) -> None:
        Prompts the user to select a store program option and dispatches the selection.

    main():
        Initializes the store instance with initial products and promotions,
        and starts the store program.
"""

import prompts
from products import Product, NonStockedProduct, LimitedProduct
from promotion import PromotionEveryXFree, PromotionDiscountPercent
from store import Store
from dispatcher import dispatcher

"""
Disclaimer: Crashes randomly after adding items to the shopping-cart.
Removed the thread-locks, but still does so. The value for "choice" is not set
sometimes. I would usually spent some time debugging the issue, but since i'm still
unwell, this has to do for now. Maybe you don't get the error while trying and can
overlook it? ;)
"""


def start(store: Store) -> None:
    """ Prompts the desired store-program and dispatches the selection. """

    while True:
        # Get validated program-selection from user.
        choice = prompts.prompt_store_menu(dispatcher)

        # Quit the program if the last option is selected
        # (not ideal, but quit should always be the last option in the list).
        if choice == len(dispatcher):
            print("Thank you for shopping at best-buy.")
            return

        # Dispatch selected option.
        print("   -----")
        dispatcher[choice - 1]["func"](store)
        print("   -----", end="\n\n")


def main():
    """ Initialises the best-buy Instance and starts the program. """

    # Available Promotions
    promotions = {
        "buy_two_get_one_free": PromotionEveryXFree("Buy two, get one free", 3),
        "twenty_percent_off": PromotionDiscountPercent("20% off", 20),
        "thirty_percent_off": PromotionDiscountPercent("30% off", 30),
        "every_second_twenty_percent": PromotionEveryXFree("Every 2nd 20%", 2, 20),
        "free": PromotionDiscountPercent("Currently free!", 100)
    }

    # setup initial stock of inventory
    product_list = [
        Product(
            "MacBook Air M2",
            price=1450,
            quantity=100,
            # promotion=promotions["twenty_percent_off"]
        ),
        Product(
            "Bose QuietComfort Earbuds",
            price=250,
            quantity=500,
            promotion=promotions["buy_two_get_one_free"]
        ),
        Product(
            "Google Pixel 7",
            price=500,
            quantity=250,
            promotion=promotions["every_second_twenty_percent"]
        ),
        NonStockedProduct(
            "Windows License",
            price=125,
            promotion=promotions["thirty_percent_off"]
        ),
        LimitedProduct(
            "Shipping",
            price=10,
            maximum=1,
            promotion=promotions["free"]
        )
    ]

    best_buy = Store(product_list)
    start(best_buy)


if __name__ == '__main__':
    main()
