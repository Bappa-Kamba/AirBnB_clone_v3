#!/usr/bin/python3
"""
    View module for the State objects
"""
from api.v1.views import app_views
from flask import jsonify
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