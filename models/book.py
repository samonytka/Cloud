from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    author = db.Column(db.String(128))
    pages_number = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, name, author, pages_number, owner_id):
        self.name = name
        self.author = author
        self.pages_number = pages_number
        self.owner_id = owner_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "pages_number": self.pages_number,
            "owner_id": self.owner_id
        }
