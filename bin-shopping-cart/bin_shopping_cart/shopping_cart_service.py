from flask import Flask, abort, request, make_response, jsonify
import uuid

# internal
from bin_shopping_cart import cart_csv
from bin_shopping_cart import product_csv
from bin_shopping_cart.discount import DiscountManager, ChairDiscount, Over1000TotalDiscount, FullSetDiscount
from bin_shopping_cart.item import Item

service = Flask(__name__)

product_dao = product_csv.ProductCsv()
discount_manager = DiscountManager([ChairDiscount(), Over1000TotalDiscount(), FullSetDiscount()])


@service.route("/api/products", methods=["GET"])
def list_product():
    return {"products": [{
        "product_id": product.id,
        "name": product.name,
        "price": product.price
    } for product in product_dao.products]}


@service.route("/api/products/<product_id>", methods=["GET"])
def get_product(product_id: str):
    product = product_dao.product(product_id)
    return {
        "product_id": product.id,
        "name": product.name,
        "price": product.price
    }


@service.route("/api/carts", methods=["POST"])
def create_cart():
    cart_id = cart_csv.create_cart()
    return {"cart_id": cart_id}


@service.route("/api/carts/<cart_id>/items/<product_id>", methods=["POST"])
def add_cart_item(cart_id, product_id):
    if not request.json:
        abort_wrong_format_body()
    if any(field not in request.json for field in ["count"]):
        abort_missing_required_field()
    try:
        product = product_dao.product(product_id)
        cart_csv.CartCsv(cart_id).add(Item(product, request.json["count"]))
        return {"message": "add item successfully"}
    except FileNotFoundError:
        abort_cart_not_found(cart_id)
    except KeyError:
        abort_product_not_found(product_id)


@service.route("/api/carts/<cart_id>/items", methods=["GET"])
def list_cart_items(cart_id):
    try:
        cart_dao = cart_csv.CartCsv(cart_id)
        return {"items": [{"product_id": item.product.id,
                           "name": item.product.name,
                           "price": item.product.price,
                           "count": item.count
                           } for item in cart_dao.items]}
    except FileNotFoundError:
        abort_cart_not_found(cart_id)


@service.route("/api/carts/<cart_id>/total", methods=["GET"])
def get_cart_total(cart_id):
    try:
        cart_dao = cart_csv.CartCsv(cart_id)
        total = cart_dao.cart.total
        discount = discount_manager.calculate(cart_dao.cart)
        return {
            "total": total,
            "discount": discount,
            "final": total - discount
        }
    except FileNotFoundError:
        abort_cart_not_found(cart_id)


@service.route("/api/carts/<cart_id>/checkout", methods=["POST"])
def checkout(cart_id):
    try:
        cart_dao = cart_csv.CartCsv(cart_id)
        cart_dao.checkout()
        return {"message": "checkout cart %s" % cart_id}
    except FileNotFoundError:
        abort_cart_not_found(cart_id)


def abort_wrong_format_body():
    abort(make_response(jsonify(message="wrong format body"), 400))


def abort_missing_required_field():
    abort(make_response(jsonify(message="missing required field"), 400))


def abort_cart_not_found(cart_id):
    abort(make_response(jsonify(message="cart %s not found" % cart_id), 404))


def abort_product_not_found(product_id):
    abort(make_response(jsonify(message="product %s not found" % product_id), 404))
