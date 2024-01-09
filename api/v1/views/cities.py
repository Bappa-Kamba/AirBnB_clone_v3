#!/usr/bin/python3
"""
    View module for City objects
"""
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    request
)
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<string:state_id>/cities", strict_slashes=False)
def cities(state_id):
    """
    Return cities object as objects using the `to_dict()` method
    """
    state = storage.get(State, state_id)
    print(state)
    if state is None:
        abort(404)
    return jsonify([
        city.to_dict() for city in state.cities
    ])


@app_views.route("/cities/<string:city_id>", strict_slashes=False)
def city(city_id):
    """
    Return a city object as JSON
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=["DELETE"])
def delete_city(city_id):
    """
    Deletes a City object by id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<string:state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city = City(**request.get_json())
    if not city.name:
        abort(400, "Missing name")
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=["PUT"])
def update_city(city_id):
    """
    Updates a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for attr, val in request.get_json().items():
        if attr not in ["id", "created_at", "updated_at"]:
            setattr(city, attr, val)
    city.save()
    return jsonify(city.to_dict()), 200
