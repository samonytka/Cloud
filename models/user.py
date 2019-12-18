from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    books = db.relationship('Book', lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "User {}".format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_books(self):
        return list(self.books)

    def to_dict(self):
        book_ids = [book.id for book in self.get_books()]

        return {
            "id": self.id,
            "name": self.name,
            "books": book_ids
        }

    @staticmethod
    def to_collection_dict():
        users = User.query.all()
        users_list = list([user.to_dict() for user in users])

        return users_list


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
