#!/usr/bin/python3
"""
Initializes the app module
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

HBNB_API_PORT = getenv("HBNB_API_PORT", 5000)
HBNB_API_HOST = getenv("HBNB_API_HOST", "0.0.0.0")

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def teardown_db(self):
    """Closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def resource_not_found(error):
    """Return a custom 404 error"""
    return jsonify({
        "error": "Not found"
        }), 404


if __name__ == '__main__':
    app.run(
        host=HBNB_API_HOST,
        port=HBNB_API_PORT,
        debug=True,
        threaded=True
    )