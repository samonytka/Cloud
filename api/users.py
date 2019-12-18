from flask import jsonify, request, url_for
from api.errors import bad_request

from app import app, db
from models.user import User


@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify(User.query.get_or_404(user_id).to_dict())


@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(User.to_collection_dict())


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}

    if 'name' not in data or 'password' not in data:
        return bad_request('must include username and password fields')
    if User.query.filter_by(name=data['name']).first():
        return bad_request('please use a different username')

    user = User(data["name"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('get_user', id=user.id)

    return response


@app.route("/api/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    if 'name' in data and data['name'] != user.name and \
            User.query.filter_by(name=data['name']).first():
        return bad_request('please use a different username')

    user.name = data["name"]
    user.set_password(data["password"])

    db.session.commit()

    return jsonify(user.to_dict())


