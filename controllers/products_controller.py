from flask import jsonify

from db import db
from models.products import Products, product_schema, products_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth


@authenticate
def product_add(req):
    post_data = req.form if req.form else req.json

    new_product = Products.get_new_product()
    populate_object(new_product, post_data)

    db.session.add(new_product)
    db.session.commit()

    return jsonify(product_schema.dump(new_product)), 201


def products_get_all(req):
    products_query = db.session.query(Products).all()

    return jsonify(products_schema.dump(products_query)), 200


def product_get_by_id(req, product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if product_query:
        return jsonify({'message': 'product found', 'product': product_schema.dump(product_query)}), 200

    else:
        return jsonify({'message': 'product not found'}), 404


@authenticate_return_auth
def product_delete_by_id(req, product_id, auth_info):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if auth_info.user.role == 'admin':
        if product_query:
            try:

                db.sesion.delete(product_query)
                db.session.commit()

            except:

                db.session.rollback()

            return jsonify('ERROR: unable to delete record'), 400

        return jsonify('product successfully deleted.'), 200

    else:
        return jsonify('unauthorized'), 401


@authenticate_return_auth
def product_update(req, product_id, auth_info):
    post_data = req.form if req.form else req.json

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if product_query:
        if auth_info.user.role == 'admin':
            populate_object(product_query, post_data)

            db.session.commit()

            return jsonify({'message': 'product updated', 'product': product_schema.dump(product_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'product not found'}), 404
