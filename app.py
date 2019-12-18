import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required


app = Flask(__name__,
            static_folder="static")
app.config.from_object(Config)
app.logger.setLevel(logging.ERROR)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"
csrf = CSRFProtect()
csrf.init_app(app)


from models.user import User
from models.book import Book

from controllers.authentication import login, registration, logout
from controllers.books import books, new_book
from api.users import *
from api.books import *


@app.route("/")
def index():
    return render_template("index.html", user=current_user)


if __name__ == '__main__':
    db.create_all()
    app.run()
