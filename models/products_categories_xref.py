from db import db


products_categories_xref = db.Table(
    "ProductsCategoriesXref",
    db.Model.metadata,
    db.Column("category_id", db.ForeignKey("Categories.category_id"), primary_key=True),
    db.Column("product_id", db.ForeignKey("Products.product_id"), primary_key=True)
)
