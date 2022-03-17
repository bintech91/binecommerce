from abc import ABC, abstractmethod

# internal
from bin_shopping_cart.cart import Cart


class Discount(ABC):
    @abstractmethod
    def calculate(self, cart: Cart) -> float:
        pass


class DiscountManager:
    def __init__(self, discounts: list[Discount]):
        self._discounts = discounts

    def calculate(self, cart: Cart) -> float:
        return max([discount.calculate(cart) for discount in self._discounts])


class ChairDiscount(Discount):
    CHAIR_PRODUCT_ID = "id-1"
    DISCOUNT_PERCENTAGE = 0.2

    def calculate(self, cart: Cart) -> float:
        item = cart.item(self.CHAIR_PRODUCT_ID)
        if item is not None and item.count >= 4:
            return round(item.product.price * item.count * self.DISCOUNT_PERCENTAGE, 4)
        return 0


class FullSetDiscount(Discount):
    CHAIR_PRODUCT_ID = "id-1"
    COUCH_PRODUCT_ID = "id-2"
    TABLE_PRODUCT_ID = "id-3"
    DESK_PRODUCT_ID = "id-4"
    DISCOUNT_PERCENTAGE = 0.17

    def calculate(self, cart: Cart) -> float:
        chair = cart.item(self.CHAIR_PRODUCT_ID)
        couch = cart.item(self.COUCH_PRODUCT_ID)
        table = cart.item(self.TABLE_PRODUCT_ID)
        desk = cart.item(self.DESK_PRODUCT_ID)

        if None in [chair, couch, table, desk]:
            return 0

        min_count = min([chair.count, couch.count, table.count, desk.count])
        if min_count == 0:
            return 0

        set_total = chair.product.price + couch.product.price + table.product.price + desk.product.price
        return round(set_total * min_count * self.DISCOUNT_PERCENTAGE, 4)


class Over1000TotalDiscount(Discount):
    DISCOUNT_PERCENTAGE = 0.15

    def calculate(self, cart: Cart) -> float:
        if cart.total > 1000:
            return round(cart.total * self.DISCOUNT_PERCENTAGE, 4)
        return 0
