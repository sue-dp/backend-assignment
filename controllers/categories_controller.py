from flask import jsonify

from db import db
from util.reflection import populate_object
from models.categories import Categories, category_schema, categories_schema
from lib.authenticate import authenticate, authenticate_return_auth


@authenticate_return_auth
def category_add(req, auth_info):
    post_data = req.form if req.form else req.json

    if auth_info.user.role == 'admin':
        new_category = Categories.get_new_category()
        populate_object(new_category, post_data)

        db.session.add(new_category)
        db.session.commit()

        return jsonify({'message': 'category added', 'category': category_schema.dump(new_category)}), 201

    else:
        return jsonify({'message': 'forbidden'}), 403


def categories_get_all(req):
    categories_query = db.session.query(Categories).all()

    return jsonify({'message': 'categories found', 'categories': categories_schema.dump(categories_query)}), 200


@authenticate
def category_get_by_id(req, category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if category_query:
        return jsonify({'message': 'category found', 'category': category_schema.dump(category_query)}), 200

    else:
        return jsonify({'message': 'category not found'}), 404


@authenticate_return_auth
def category_delete_by_id(req, category_id, auth_info):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if auth_info.user.role == 'admin':
        if category_query:

            db.session.delete(category_query)
            db.session.commit()

            return jsonify({'message': 'record successfully deleted'}), 200

        return jsonify({'message': 'category not found'}), 404

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def category_update(req, category_id, auth_info):
    post_data = req.form if req.form else req.json

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if category_query:
        if auth_info.user.role == 'admin':
            populate_object(category_query, post_data)

            db.session.commit()

            return jsonify({'message': 'category updated', 'category': category_schema.dump(category_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'category not found'}), 404


@authenticate_return_auth
def category_activity(req, category_id, auth_info):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if category_query:
        if auth_info.user.role == 'admin':
            category_query.active = not category_query.active

            db.session.commit()

            return jsonify({'message': 'category activity has been updated', 'category': category_schema.dump(category_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'category not found'}), 404
