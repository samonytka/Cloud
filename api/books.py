from flask import jsonify, request, url_for

from api.errors import bad_request, error_response
from app import app, db, csrf
from models.book import Book
from models.user import User


@app.route("/api/users/<user_id>/books", methods=["GET"])
def get_books_api(user_id):
    user = User.query.get_or_404(user_id)

    books = Book.query.filter_by(owner_id=user_id)
    books_list = list([book.to_dict() for book in books])

    return jsonify(books_list)


@app.route("/api/users/<user_id>/books/<book_id>", methods=["GET"])
def get_book_api(user_id, book_id):
    user = User.query.get_or_404(user_id)

    book = Book.query.filter_by(owner_id=user_id, id=book_id).first()
    if book is None:
        return error_response(404, "book {} not found".format(book_id))

    return jsonify(book.to_dict())


@app.route("/api/users/<user_id>/books", methods=["POST"])
@csrf.exempt
def add_book_api(user_id):
    user = User.query.get_or_404(user_id)

    data = request.get_json() or {}

    required_fields = ("name", "author", "pages_number")
    for field in required_fields:
        if field not in data.keys():
            return bad_request("Must contain {} field".format(field))

    book = Book(data["name"], data["author"], data["pages_number"], user_id)
    db.session.add(book)
    db.session.commit()

    response = jsonify(book.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('get_book_api', user_id=user_id, book_id=book.id)

    return response


@app.route("/api/users/<user_id>/books/<book_id>", methods=["PUT"])
@csrf.exempt
def update_book_api(user_id, book_id):
    user = User.query.get_or_404(user_id)
    book = Book.query.get_or_404(book_id)

    data = request.get_json() or {}
    required_fields = ("name", "author", "pages_number")
    for field in required_fields:
        if field not in data.keys():
            return bad_request("Must contain {} field".format(field))

    book.name = data["name"]
    book.author = data["author"]
    book.pages_number = data["pages_number"]

    db.session.commit()

    return jsonify(book.to_dict())


@app.route("/api/users/<user_id>/books/<book_id>", methods=["DELETE"])
@csrf.exempt
def delete_book_api(user_id, book_id):
    user = User.query.get_or_404(user_id)
    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    response = jsonify({})
    response.status_code = 201

    return response
