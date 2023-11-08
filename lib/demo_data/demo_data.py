import sys

from db import db
from models.users import Users
from lib.demo_data.user_demo_data import add_user_demo_data
from lib.demo_data.products_demo_data import add_product_demo_data


def run_demo_data():
    user_query = db.session.query(Users).filter(Users.first_name == 'Barney').first()

    if len(sys.argv) > 1 and sys.argv[1] == 'demo-data':
        if user_query == None:
            print('Creating demo data...')
            add_user_demo_data()
            add_product_demo_data()
        else:
            print('Demo data found.')
