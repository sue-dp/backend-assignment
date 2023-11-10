import config
from db import db
from models.categories import Categories


def add_category_demo_data():
    for category in config.categories:

        new_category = db.session.query(Categories).filter(Categories.category_name == category).first()

        if new_category == None:
            category_name = category
            active = True

            new_category = Categories(category_name, active)

            db.session.add(new_category)

    db.session.commit()
