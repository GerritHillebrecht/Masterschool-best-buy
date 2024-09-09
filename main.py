import prompts
from products import Product
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
            print("Goodbye")
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
        Product("Google Pixel 7", price=500, quantity=250)
    ]
    best_buy = Store(product_list)

    start(best_buy)


if __name__ == '__main__':
    main()
