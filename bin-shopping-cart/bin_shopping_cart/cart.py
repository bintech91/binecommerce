from typing import Optional

# internal
from bin_shopping_cart.item import Item


class Cart:
    def __init__(self, cart_id: str):
        self._cart_id = cart_id
        self._items: dict[str, Item] = {}

    def add(self, item: Item):
        self._items[item.product.id] = item

    def remove(self, product_id):
        if product_id in self._items:
            del self._items[product_id]

    def item(self, product_id) -> Optional[Item]:
        if product_id in self._items:
            return self._items[product_id]
        return None

    @property
    def total(self) -> float:
        list_subtotal = [item.product.price * item.count for item in self.items]
        return round(sum(list_subtotal),4)

    @property
    def cart_id(self) -> str:
        return self._cart_id

    @property
    def items(self) -> list[Item]:
        return list(self._items.values())
