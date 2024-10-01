#!/usr/bin/env python3
"""
Flask app
"""

from auth import Auth
from flask import Flask, jsonify
from flask import request


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users() -> None:
    """
    Registers a user
    """
    email = request.form['email']
    password = request.form['password']
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": email, "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0", port="5000")
