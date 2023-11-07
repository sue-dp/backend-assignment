import config
from db import db
from models.products import Products


def add_product_demo_data():
    for product in config.products:

        new_product = db.session.query(Products).filter(Products.product_name == product).first()

        if new_product == None:
            product_name = product

            new_product = Products(product_name)

            db.session.add(new_product)

    db.session.commit()
