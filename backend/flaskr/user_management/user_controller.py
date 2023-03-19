from flask import Blueprint, Response, jsonify


users_routes = Blueprint("users_routes", __name__, url_prefix="/users")


@users_routes.route("/login")
def login():
  pass
