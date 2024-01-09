#!/usr/bin/python3
"""
    View module for User objects
"""
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    request
)
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def users():
    """
    Return users object as objects using the `to_dict()` method
    """
    return jsonify([
        user.to_dict() for user in storage.all(User).values()
        ])


@app_views.route("/users/<string:user_id>", strict_slashes=False)
def user(user_id):
    """
    Return a user object as JSON
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                    strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object by id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    Creates a User
    """
    if not request.is_json:
        abort(400, "Not a JSON")

    user = User(**request.get_json())
    if not user.email:
        abort(400, "Missing email")
    if not user.password:
        abort(400, "Missing password")
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<string:user_id>", methods=["PUT"],
                    strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")

    for k, v in request.get_json().items():
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200
