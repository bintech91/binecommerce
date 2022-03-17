# standard
import csv

# internal
from bin_shopping_cart.product import Product


class ProductCsv:
    PRODUCT_CSV = "data/product.csv"

    def __init__(self):
        self._products: dict[str, Product] = {}
        with open(self.PRODUCT_CSV, "r+") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                product = Product(row[0], row[1], float(row[2]))
                self._products[product.id] = product

    def add(self, product: Product):
        self._products[product.id] = product
        self.__sync()

    def product(self, product_id) -> Product:
        return self._products[product_id]

    @property
    def products(self) -> list[Product]:
        return list(self._products.values())

    def __sync(self):
        csv_items = [[product.id, product.name, product.price] for product in self._products.values()]
        with open(self.PRODUCT_CSV, "w+") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_items)


if __name__ == '__main__':
    product_csv = ProductCsv()
    product_csv.add(Product("id-5", "test", 123.00))
