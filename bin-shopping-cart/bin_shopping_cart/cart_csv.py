# standard
import csv
from pathlib import Path
import shutil
import uuid

# internal
from bin_shopping_cart.cart import Cart
from bin_shopping_cart.item import Item
from bin_shopping_cart.product import Product


def create_cart():
    cart_id = str(uuid.uuid4())
    path = CartCsv.CART_CSV_PATTERN % cart_id
    Path(path).touch(exist_ok=True)
    return cart_id


class CartCsv:
    CART_CSV_PATTERN = "data/carts/%s.csv"
    ORDER_CSV = "data/orders/"

    def __init__(self, cart_id: str):
        self._cart = Cart(cart_id)
        with open(self.CART_CSV_PATTERN % cart_id, "r+") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                product = Product(row[0], row[1], float(row[2]))
                item = Item(product, int(row[3]))
                self._cart.add(item)

    def add(self, item: Item):
        self._cart.add(item)
        self.__sync()

    def checkout(self):
        shutil.move(self.CART_CSV_PATTERN % self._cart.cart_id, self.ORDER_CSV)

    def __sync(self):
        csv_items = [[item.product.id, item.product.name, item.product.price, item.count] for item in self._cart.items]
        with open(self.CART_CSV_PATTERN % self._cart.cart_id, "w+") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_items)

    @property
    def items(self) -> list[Item]:
        return self._cart.items

    @property
    def cart(self) -> Cart:
        return self._cart
