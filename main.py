"""
main module

This module initializes the store with a list of products and starts the store program.
It includes functions to start the program and initialize the store inventory.

Functions:
    start(store: Store) -> None:
        Prompts the user to select a store program option and dispatches the selection.

    main():
        Initializes the store instance with initial products and starts the store program.
"""


import prompts
from products import Product, NonStockedProduct, LimitedProduct
from store import Store
from dispatcher import dispatcher


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
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, maximum=1)
    ]
    best_buy = Store(product_list)

    start(best_buy)


if __name__ == '__main__':
    main()
