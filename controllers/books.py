from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app import app, db
from forms.book_form import UpdateBookForm, DeleteBookForm
from models.book import Book


@app.route("/books")
@login_required
def books():
    books = current_user.books
    new_book_form = UpdateBookForm()

    return render_template("book/books.html", title="Books", books=books, new_book_form=new_book_form)


@app.route("/books/new", methods=["POST"])
@login_required
def new_book():
    form = UpdateBookForm()
    if form.validate_on_submit():
        name = form.name.data
        author = form.author.data
        pages_number = form.pages_number.data
        owner_id = current_user.id
        book = Book(name, author, pages_number, owner_id)

        db.session.add(book)
        db.session.commit()

        return redirect(url_for("books"))

    return render_template("book/books.html", new_book_form=form)


@app.route("/books/update/<book_id>", methods=["GET"])
@login_required
def update_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    form = UpdateBookForm(obj=book)

    return render_template("book/update.html", plant_id=book_id, form=form)


@app.route("/books/update", methods=["POST"])
@login_required
def do_update():
    form = UpdateBookForm()
    if form.validate_on_submit():
        book = Book.query.filter_by(id=form.id.data).first()
        book.name = form.name.data
        book.author = form.author.data
        book.pages_number = form.pages_number.data

        db.session.commit()

        return redirect(url_for("books"))

    return render_template("book/update.html", form=form)


@app.route("/books/delete/<book_id>", methods=["GET"])
@login_required
def delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    form = DeleteBookForm(obj=book)

    return render_template("book/delete.html", form=form, book=book)


@app.route("/books/delete", methods=["POST"])
@login_required
def do_delete():
    form = DeleteBookForm()
    if form.validate_on_submit():
        book = Book.query.filter_by(id=form.id.data).first()
        db.session.delete(book)
        db.session.commit()

        return redirect(url_for("books"))

    return render_template("book/delete.html", form=form)
