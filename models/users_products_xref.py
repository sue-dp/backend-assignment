from db import db


users_products_xref = db.Table(
    "UsersProductsXref",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("Users.user_id"), primary_key=True),
    db.Column("product_id", db.ForeignKey("Products.product_id"), primary_key=True)
)
