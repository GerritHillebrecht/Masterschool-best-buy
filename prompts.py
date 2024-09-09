from dispatcher import DispatcherList
from store import Store
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
            print(f"{idx + 1}. {disp["label"]}")

        choice = prompt_integer(
            "Please choose a number: ",
            "Please enter your selection as a number."
        )

        if not 1 <= choice <= len(dispatcher):
            print(f"Please select a number from 1 to {len(dispatcher)}")
            continue

        return choice


def prompt_order_item(store: Store) -> Product | None:
    """
    Prompts the user for the item(s) he wants to buy. Loops until an empty string is given.
    Returns None if an empty string is given. Items are selected by index, input is validated.
    :param store: The store instance.
    :return: The selected product instance, None if empty string is given.
    """
    available_products = store.get_all_products()
    while True:
        for idx, product in enumerate(available_products):
            print(f"{idx + 1}. {product.name}")

        try:
            selection = input("Which product # do you want? ")

            if len(selection) == 0:
                return None

            choice = int(selection)

        except ValueError:
            print(f"Select an available Product by entering a number")
            continue

        if not 1 <= choice <= len(available_products):
            print(f"Select a product within 1 and {len(available_products)}")

        return available_products[choice - 1]


def prompt_order_item_quantity(product: Product) -> int:
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

        available_stock = product.get_quantity()
        if not 0 <= quantity <= available_stock:
            print(f"Select a quantity between 0 and {available_stock}.")
            continue

        return quantity


def prompt_shopping_list(store) -> list[tuple[Product, int]]:
    """
    Prompts the user for a shopping list by listing all available
    products and prompting the quantity the user wants to acquire.
    :param store: The store instance.
    :return: Returns the shopping list as a of tuples (product, quantity).
    """
    shopping_list = []
    while True:
        order_item = prompt_order_item(store)

        if order_item is None:
            return shopping_list

        quantity = prompt_order_item_quantity(order_item)
        shopping_list.append((order_item, quantity))


def prompt_integer(
        input_text="Please enter a number: ",
        error_text="Your input is not convertable to an integer."
) -> int:
    """
    Queries the user for an integer. Loops until valid input is given.
    :param input_text: [Optional]: The input-query text displayed to the user.
    :param error_text: [Optional]: The message the user receives upon non-convertable input.
    :return: The converted string.
    """
    while True:
        try:
            quantity = int(input(input_text))
        except ValueError:
            print(error_text)
            continue

        return quantity
