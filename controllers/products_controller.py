from flask import jsonify

from db import db
from models.products import Products, product_schema, products_schema
from util.reflection import populate_object


def product_add(req):
    post_data = req.form if req.form else req.json

    new_product = Products.get_new_product()
    populate_object(new_product, post_data)

    db.session.add(new_product)
    db.session.commit()

    return jsonify(product_schema.dump(new_product)), 201


def products_get_all():
    products_query = db.session.query(Products).all()

    return jsonify(products_schema.dump(products_query)), 200


def product_delete_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    db.session.delete(product_query)
    db.session.commit()

    return jsonify({"message": "product deleted"}), 200
