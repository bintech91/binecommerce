
class Product:
    def __init__(self, product_id: str, name: str, price: float):
        self._product_id = product_id
        self._name = name
        self._price = price

    @property
    def id(self) -> str:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, price: float):
        self._price = price

