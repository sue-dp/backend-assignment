from flask import jsonify

from db import db
from models.users import Users, user_schema, users_schema
from models.products import Products
from util.reflection import populate_object
from lib.authenticate import authenticate

# @authenticate_return_auth


def user_add(req):
    # def user_add(req, auth_info):
    post_data = req.form if req.form else req.json

    # if auth_info.user.role =='super-admin':
    new_user = Users.get_new_user()
    populate_object(new_user, post_data)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201
# else:
#     return jsonify("your role isn't cool enough")


@authenticate
def users_get_all(req):
    users_query = db.session.query(Users).all()

    return jsonify(users_schema.dump(users_query)), 200


def user_add_product(req):
    post_data = req.form if req.form else req.json
    user_id = post_data.get("user_id")
    product_id = post_data.get("product_id")

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if user_query and product_query:
        user_query.products.append(product_query)
        db.session.commit()

        return jsonify({"message": "product added to user", "user": user_schema.dump(user_query)}), 201
    else:
        return jsonify("not found"), 404
