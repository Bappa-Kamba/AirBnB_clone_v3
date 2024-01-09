#!/usr/bin/python3
"""
    View module for Review objects
"""
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    request
)
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<string:place_id>/reviews", strict_slashes=False)
def reviews(place_id):
    """
    Return reviews object as objects using the `to_dict()` method
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([
        review.to_dict() for review in place.reviews
    ])


@app_views.route("/reviews/<string:review_id>", strict_slashes=False)
def review(review_id):
    """
    Return a review object as JSON
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<string:review_id>", methods=["DELETE"])
def delete_review(review_id):
    """
    Deletes a Review object by id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<string:place_id>/reviews", methods=["POST"],
                    strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")

    review = Review(**request.get_json())
    if not review.text:
        abort(400, "Missing text")
    if not review.user_id:
        abort(400, "Missing user_id")
    if not storage.get(User, review.user_id):
        abort(404)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<string:review_id>", methods=["PUT"],
                    strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
