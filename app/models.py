from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


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

