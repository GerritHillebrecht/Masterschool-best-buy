"""
prompts module

This module provides functions to prompt the user for various inputs related to store operations. It includes functions to prompt for menu selections, product selections, and quantities, as well as a utility function to prompt for integers.

Functions:
    prompt_store_menu(dispatcher: DispatcherList) -> int:
        Prompts the user for a selection from the store menu and returns the selected option index.

    prompt_order_item(store) -> Product | None:
        Prompts the user to select an item to buy from the store and returns the selected product instance.

    prompt_order_item_quantity(product: Product) -> int | None:
        Prompts the user for the quantity of the selected product to buy and returns the validated quantity.

    prompt_integer(input_text="Please enter a number: ", error_text="Your input is not convertable to an integer.") -> int | None:
        Prompts the user for an integer input and returns the converted integer.
"""

from dispatcher import DispatcherList
from products import Product


def prompt_store_menu(dispatcher: DispatcherList) -> int:
    """
    Prompts the user for a selection of the store menu. The store menu consists of
    all available store functions. Keeps prompting until a valid input is received.
    :param dispatcher: The dispatcher of the store-methods.
    :return: The selected dispatcher-function-index.
    """
    while True:
        # Print menu
        print("   Store Menu\n   ----------")
        for idx, disp in enumerate(dispatcher):
            print(f'{idx + 1}. {disp["label"]}')

        choice = prompt_integer(
            "Please choose a number: ",
            "Please enter your selection as a number."
        )

        if not 1 <= choice <= len(dispatcher):
            print(f"Please select a number from 1 to {len(dispatcher)}")
            continue

        return choice


def prompt_order_item(store) -> Product | None:
    """
    Prompts the user for the item(s) he wants to buy. Loops until an empty string is given.
    Returns None if an empty string is given. Items are selected by index, input is validated.
    :param store: The store instance.
    :return: The selected product instance, returns None if string is empty.
    """
    shopping_cart = store.shopping_cart

    while True:
        # Fetch product quantity every time the user gets prompted for accurate in-stock-data.
        available_products: list[Product] = list(
            filter(
                lambda item: (item.quantity - shopping_cart[item.name]) > 0,
                store.get_all_available_products_for_current_cart()
            )
        )

        for idx, product in enumerate(available_products):
            print(f"{idx + 1}. {product.name}")

        try:
            selection = input("Which product # do you want? ")

            if len(selection) == 0:
                return None

            choice = int(selection)

        except ValueError:
            print("Select an available Product by entering a number")
            continue

        if not 1 <= choice <= len(available_products):
            print(f"Select a product within 1 and {len(available_products)}")
            continue

        return available_products[choice - 1]


def prompt_order_item_quantity(product: Product) -> int | None:
    """
    Prompts the user for a quantity he wants to buy. Zero is allowed to easier compensate for
    user-errors (accidental wrong product selection). Loops until valid input is given. Limits
    the quantity to available stock.
    :param product: The selected product by the user. Needed to get the available stock.
    :return: The validated quantity selected by the user.
    """
    while True:
        quantity = prompt_integer(
            "What amount do you want? ",
            "Select a quantity by entering a number"
        )

        available_stock = product.quantity

        if quantity is None:
            return None

        if not 0 <= quantity <= available_stock:
            print(f"Select a quantity between 0 and {available_stock}.")
            continue

        return quantity


def prompt_integer(
        input_text="Please enter a number: ",
        error_text="Your input is not convertable to an integer."
) -> int | None:
    """
    Queries the user for an integer. Loops until valid input is given.
    :param input_text: [Optional]: The input-query text displayed to the user.
    :param error_text: [Optional]: The message the user receives upon non-convertable input.
    :return: The converted string.
    """
    while True:
        try:
            user_input = input(input_text)

            # exit prompt
            if not len(user_input):
                return None

            quantity = int(user_input)
        except ValueError:
            print(error_text)
            continue

        return quantity
