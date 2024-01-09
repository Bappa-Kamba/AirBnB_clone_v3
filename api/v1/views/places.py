#!/usr/bin/python3
"""
    View module for Place objects
"""
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    request
)
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<string:city_id>/places", strict_slashes=False)
def places(city_id):
    """
    Return places object as objects using the `to_dict()` method
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([
        place.to_dict() for place in city.places
    ])


@app_views.route("/places/<string:place_id>", strict_slashes=False)
def place(place_id):
    """
    Return a place object as JSON
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=["DELETE"])
def delete_place(place_id):
    """
    Deletes a Place object by id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<string:city_id>/places", methods=["POST"],
                    strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")

    place = Place(**request.get_json())
    if not place.user_id:
        abort(400, "Missing user_id")
    user = storage.get(User, place.user_id)
    if not user:
        abort(404)
    if not place.name:
        abort(400, "Missing name")
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<string:place_id>", methods=["PUT"],
                    strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
