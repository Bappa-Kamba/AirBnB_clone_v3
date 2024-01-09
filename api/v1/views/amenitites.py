#!/usr/bin/python3
"""
    View module for Amenity objects
"""
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    request
)
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def amenities():
    """
    Return amenities object as objects using the `to_dict()` method
    """
    return jsonify([
        amenity.to_dict() for amenity in storage.all(Amenity).values()
        ])


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False)
def amenity(amenity_id):
    """
    Return a amenity object as JSON
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities", methods={"POST"}, 
                 strict_slash=False)
def create_amenity():
    """
    Creates an Amenity for a Place
    """
    amenity = Amenity(**request.get_json())
    if not amenity.name:
        abort(400, "Missing name")
    amenity.save()
    return jsonify(amenity.to_dict()), 201


