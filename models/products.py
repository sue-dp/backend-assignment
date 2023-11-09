import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .users_products_xref import users_products_xref
from .products_categories_xref import products_categories_xref


class Products(db.Model):
    __tablename__ = "Products"

    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = db.Column(db.String(), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)

    users = db.relationship("Users", secondary=users_products_xref, back_populates="products")
    categories = db.relationship("Categories", secondary=products_categories_xref, back_populates="products")

    def __init__(self, product_name, active):
        self.product_name = product_name
        self.active = active

    def get_new_product():
        return Products("", True)


class ProductsSchema(ma.Schema):
    class Meta:
        fields = ['product_id', 'product_name', 'users', 'categories', 'active']

    users = ma.fields.Nested("UsersSchema", many=True, exclude=["products"])
    categories = ma.fields.Nested("CategoriesSchema", many=True, exclud=['products'])


product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)
