"""
dispatcher module

This module provides a type definition for the dispatcher and a list of dispatcher actions. Each action is mapped to a label and a corresponding function to manage store operations.

Classes:
    Dispatcher

Type Aliases:
    DispatcherList

Variables:
    dispatcher: list[Dispatcher]
        A list of dispatcher actions mapping labels to functions.
"""

from typing import Callable, TypedDict


class Dispatcher(TypedDict):
    """
    Type-definition for the dispatcher.
    """
    label: str
    func: Callable


DispatcherList = list[Dispatcher]

dispatcher = [
    {
        "label": "List all products in store",
        "func": lambda store: store.show_all_products()
    },
    {
        "label": "Show total amount in store",
        "func": lambda store: print(
            f"Total of {len(store)} items in store."
        )
    },
    {
        "label": "Make an order",
        "func": lambda store: store.start_order()
    },
    {
        "label": "Quit", "func":
        lambda store: None
    },
]
