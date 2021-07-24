from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login
from datetime import datetime


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    full_name = db.Column(db.String(100))
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def set_password(self, form_password):
        self.password = generate_password_hash(form_password)

    def verify_password(self, form_password):
        return check_password_hash(self.password, form_password)

    def __repr__(self):
        return "<User: Id equals {} and email equals {}>".format(self.id, self.email)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    precedence = db.Column(db.Integer)
    name = db.Column(db.String(30))
    users = db.relationship("User", backref="user", lazy="dynamic")

    def __repr__(self):
        return "<Role: Id is {} and precedence is {} using name {}>".format(self.id, self.precedence, self.name)


ordered_items = db.Table("ordered_items",
                          db.Column("order_id", db.Integer, db.ForeignKey("orders.id")),
                          db.Column("item_id", db.Integer, db.ForeignKey("items.id"))
                          )


class Order(db.Model):

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    datetimestamp = db.Column(db.DateTime, default=datetime.utcnow())
    price = db.Column(db.Float)

    def __repr__(self):
        return "<Order: Id is {}>".format(self.id)


class Item(db.Model):
    """
    Exemplo: Pizza de muçarela - ou seja, um produto!
    """
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    volume = db.Column(db.Float)
    description = db.Column(db.String(60))
    orders = db.relationship("Order", secondary=ordered_items, backref=db.backref("order_item", lazy="dynamic"))

    def __repr__(self):
        return "<Item: Id is {} and description is {}>".format(self.id, self.description)


class Material(db.Model):
    """
    Material que compõe um produto(item)
    """

    __tablename__ = "materials"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(60))

    def __repr__(self):
        return "<Material: Id is {} and name is {}>".format(self.id, self.name
