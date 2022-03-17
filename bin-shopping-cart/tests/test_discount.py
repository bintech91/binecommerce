from bin_shopping_cart.product import Product
from bin_shopping_cart.cart import Cart
from bin_shopping_cart.item import Item
from bin_shopping_cart.discount import DiscountManager, ChairDiscount, FullSetDiscount, Over1000TotalDiscount

# id-1,Chair,100.01
# id-2,Couch,749.99
# id-3,Table,249.90
# id-4,Desk,500.10

chair_product = Product("id-1", "Chair", 100.01)
couch_product = Product("id-2", "Couch", 749.99)
table_product = Product("id-3", "Table", 249.90)
desk_product = Product("id-4", "Desk", 500.10)


def test_chair_with_discount():
    cart = Cart(cart_id="test")
    cart.add(Item(chair_product, 10))
    assert (chair_product.price * 10 * 0.2 == ChairDiscount().calculate(cart))


def test_chair_without_discount():
    cart = Cart(cart_id="test")
    cart.add(Item(chair_product, 1))
    assert (ChairDiscount().calculate(cart) == 0)


def test_fullset_with_discount():
    cart = Cart(cart_id="test")
    cart.add(Item(chair_product, 3))
    cart.add(Item(couch_product, 4))
    cart.add(Item(table_product, 5))
    cart.add(Item(desk_product, 6))
    assert (FullSetDiscount().calculate(cart) == float(816))


def test_fullset_without_discount():
    cart = Cart(cart_id="test")
    cart.add(Item(chair_product, 3))
    cart.add(Item(couch_product, 4))
    cart.add(Item(table_product, 5))
    assert (FullSetDiscount().calculate(cart) == 0)


def test_over_1000_with_discount():
    cart = Cart(cart_id="test")
    cart.add(Item(chair_product, 1))
    cart.add(Item(couch_product, 1))
    cart.add(Item(table_product, 1))
    cart.add(Item(desk_product, 1))
    assert (Over1000TotalDiscount().calculate(cart) == float(240))


def test_over_1000_without_discount():
    cart = Cart(cart_id="test")
    cart.add(Item(chair_product, 1))
    assert (Over1000TotalDiscount().calculate(cart) == 0)


def test_discount_manager_chair_discount():
    cart = Cart(cart_id="test")
    cart.add(Item(chair_product, 1000))
    cart.add(Item(couch_product, 1))
    cart.add(Item(table_product, 1))
    cart.add(Item(desk_product, 1))
    assert (DiscountManager([ChairDiscount(), FullSetDiscount(), Over1000TotalDiscount()]).calculate(cart)
            == ChairDiscount().calculate(cart))


def test_discount_manager_fullset_discount():
    cart = Cart(cart_id="test")
    cart.add(Item(chair_product, 20))
    cart.add(Item(couch_product, 20))
    cart.add(Item(table_product, 20))
    cart.add(Item(desk_product, 20))
    assert (DiscountManager([ChairDiscount(), FullSetDiscount(), Over1000TotalDiscount()]).calculate(cart)
            == FullSetDiscount().calculate(cart))


def test_discount_manager_over_1000_discount():
    cart = Cart(cart_id="test")
    cart.add(Item(chair_product, 1))
    cart.add(Item(couch_product, 1))
    cart.add(Item(table_product, 1))
    assert (DiscountManager([ChairDiscount(), FullSetDiscount(), Over1000TotalDiscount()]).calculate(cart)
            == Over1000TotalDiscount().calculate(cart))
