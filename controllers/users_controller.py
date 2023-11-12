from flask import jsonify

from db import db
from models.users import Users, user_schema, users_schema
from models.products import Products
from models.auth_tokens import AuthTokens
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth


@authenticate_return_auth
def user_add(req, auth_info):
    post_data = req.form if req.form else req.json

    if auth_info.user.role == 'admin':
        new_user = Users.get_new_user()
        populate_object(new_user, post_data)

        db.session.add(new_user)
        db.session.commit()

        return jsonify(user_schema.dump(new_user)), 201
    else:
        return jsonify('unauthorized'), 401


@authenticate_return_auth
def users_get_all(req, auth_info):
    users_query = db.session.query(Users).all()
    print(auth_info.user.role)

    if auth_info.user.role == 'admin':
        return jsonify({'message': 'users found', 'users': users_schema.dump(users_query)}), 200
    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def user_get_by_id(req, user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user_query:
        if auth_info.user.role == 'admin' or user_id == auth_info.user.user_id:
            return jsonify({'message': 'user found', 'user': user_schema.dump(user_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401
    else:
        return jsonify({'message': 'user not found'}), 404


@authenticate_return_auth
def user_delete_by_id(req, user_id, auth_info):
    if auth_info.user.user_id == user_id:
        return jsonify({'message': 'user cannot delete themselves'}), 403

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if auth_info.user.role == 'admin':
        if user_query:
            auth_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_id).all()
            for token in auth_tokens:
                db.session.delete(token)
            db.session.delete(user_query)
            db.session.commit()

            return jsonify({'message': 'record successfully deleted'}), 200

        return jsonify({'message': 'user not found'}), 404

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def user_update(req, user_id, auth_info):
    post_data = req.form if req.form else req.json

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user_query:
        if auth_info.user.role == 'admin' or user_id == auth_info.user.user_id:
            populate_object(user_query, post_data)

            db.session.commit()

            return jsonify({'message': 'user updated', 'user': user_schema.dump(user_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'user not found'}), 404


@authenticate_return_auth
def user_add_product(req, auth_info):
    post_data = req.form if req.form else req.json
    user_id = auth_info.user.user_id
    product_id = post_data.get('product_id')

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if user_query and product_query:
        user_query.products.append(product_query)
        db.session.commit()

        return jsonify({'message': 'product added to user', 'user': user_schema.dump(user_query)}), 201

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def user_activity(req, user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user_query:
        if auth_info.user.role == 'admin':
            user_query.active = not user_query.active

            db.session.commit()

            return jsonify({'message': 'user activity has been updated', 'user': user_schema.dump(user_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'user not found'}), 404
