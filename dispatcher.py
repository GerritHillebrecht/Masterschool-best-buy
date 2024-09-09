from typing import Callable, TypedDict
from store import Store
import prompts


class Dispatcher(TypedDict):
    label: str
    func: Callable


DispatcherList = list[Dispatcher]


def make_an_order(store: Store) -> None:
    """
    Prompts the user for a shopping-list. The shopping-list is given to store instance.
    Prints the price of the order.
    :param store: The store instance.
    :return: Prints the price
    """
    # Only show list if there's active products
    if len(store.get_all_products()) == 0:
        return

    # Prompt (loop) for shopping_list
    shopping_list = prompts.prompt_shopping_list(store)

    # Order the list
    price = store.order(shopping_list)

    print("********")
    print(f"Order made! Total payment: ${price}")


def list_all_products(store: Store) -> None:
    """
    Prints all Product data of available products.
    :param store: The store instance.
    :return: Prints the product information of all available products.
    """
    product_infos = [
        product.show()
        for product in store.get_all_products()
    ]

    for idx, product_info in enumerate(product_infos):
        print(f"{idx + 1}. {product_info}")


dispatcher = [
    {
        "label": "List all products in store",
        "func": list_all_products
    },
    {
        "label": "Show total amount in store",
        "func": lambda store: print(
            f"Total of {store.get_total_quantity()} items in store."
        )
    },
    {
        "label": "Make an order",
        "func": make_an_order
    },
    {
        "label": "Quit", "func":
        lambda store: store
    },
]
