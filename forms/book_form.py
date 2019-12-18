from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired


class DeleteBookForm(FlaskForm):
    id = HiddenField()
    submit = SubmitField("Delete")


class UpdateBookForm(FlaskForm):
    id = HiddenField()
    name = StringField("Book Name", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    pages_number = IntegerField("Pages Number", validators=[DataRequired()])

    submit = SubmitField("Add")
