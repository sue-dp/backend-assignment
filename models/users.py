import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from models.users_products_xref import users_products_xref


class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), default="user", nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    products = db.relationship("Products", secondary=users_products_xref, back_populates="users")

    def __init__(self, first_name, last_name, email, password, role="user", active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role
        self.active = active

    def get_new_user():
        return Users("", "", "", "", "user", True)


class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'first_name', 'last_name', 'email', 'role', 'active', 'products']

    products = ma.fields.Nested("ProductsSchema", many=True, exclude=["users"])


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
# returns a list of dictionaries
