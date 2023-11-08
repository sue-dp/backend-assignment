from flask import request, Blueprint

import controllers


products = Blueprint('products', __name__)


@products.route("/product", methods=["POST"])
def product_add():
    return controllers.product_add(request)


@products.route("/products", methods=["GET"])
def products_get_all():
    return controllers.products_get_all(request)


@products.route('/product/<product_id>', methods=['GET'])
def product_get_by_id(product_id):
    return controllers.product_get_by_id(request, product_id)


@products.route("/product/<product_id>", methods=["DELETE"])
def product_delete_by_id(product_id):
    return controllers.product_delete_by_id(request, product_id)


@products.route('/product/<product_id>', methods=['PUT'])
def product_update(product_id):
    return controllers.product_update(request, product_id)
