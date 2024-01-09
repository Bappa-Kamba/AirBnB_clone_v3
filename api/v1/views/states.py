#!/usr/bin/python3
"""
    View module for the State objects
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def states():
    """
    Return states object as objects using the `to_dict()` method
    """
    return jsonify([
        state.to_dict() for state in storage.all(State).values()
        ])


@app_views.route("/states/<string:state_id>", strict_slashes=False)
def state(state_id):
    """
    Return a state object as JSON
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                    strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object by id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Creates a State
    """
    state = State(**request.get_json())
    if not state.name:
        abort(400, "Missing name")
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<string:state_id>", methods=["PUT"],
                    strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
