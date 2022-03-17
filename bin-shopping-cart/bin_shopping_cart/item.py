from bin_shopping_cart.product import Product


class Item:
    def __init__(self, product: Product, count: int):
        self._product = product
        self._count = count

    @property
    def product(self) -> Product:
        return self._product

    @property
    def count(self) -> int:
        return self._count
