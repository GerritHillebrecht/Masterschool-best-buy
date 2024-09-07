from products import Product
from store import Store
from typing import Callable

ProgramChoices = list[tuple[str, Callable]]
ProductList = list[Product]


def prompt_store_menu(program_choices: ProgramChoices) -> int:
    """
        Prompts the user for a selection of the store menu. The store menu consists of
        all available store functions. Keeps prompting the user until a valid input is received.
     """
    while True:
        print("   Store Menu\n   ----------")
        for idx, (label, func) in enumerate(program_choices):
            print(f"{idx + 1}. {label}")

        try:
            choice = int(input("Please choose a number: "))
        except ValueError:
            print(f"Please enter your selection as a number.")
            continue

        if not 1 <= choice <= len(program_choices):
            print(f"Please select a number from 1 to {len(program_choices)}")
            continue

        return choice


def start(
        product_list: ProductList,
        program_choices: ProgramChoices
) -> None:
    """ Starts the program. """

    # Get validated program selection from user
    choice = prompt_store_menu(program_choices)
    print(choice)


def main():
    # setup initial stock of inventory
    product_list: ProductList = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250)
    ]
    best_buy = Store(product_list)

    # program-choices
    program_choices = [
        ("List all products in store", lambda x: x),
        ("Show total amount in store", lambda x: x),
        ("Make an order", lambda x: x),
        ("Quit", lambda x: x),
    ]

    start(product_list, program_choices)


if __name__ == '__main__':
    main()
