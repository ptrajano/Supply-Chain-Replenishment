from Product import Product
from typing import Callable

class Day:
    def __init__(self,
                 foo_stock: Callable[[Product, int], int],
                 foo_movement: Callable[[Product], int],) -> None:
        ... 
