from src.storage.flat import Flat
from typing import List

Flats = List[Flat]


# todo make filter as separate essence
class BaseParser:
    def set_min_price(self, price: int):
        raise MethodNotImplemented()

    def set_max_price(self, price: int):
        raise MethodNotImplemented()

    def get_all(self) -> Flats:
        raise MethodNotImplemented()


class MethodNotImplemented(Exception):
    pass
