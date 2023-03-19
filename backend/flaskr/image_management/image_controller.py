import os
from flask import Blueprint, Response, jsonify


images_routes = Blueprint("images_routes", __name__, url_prefix="/images")


@images_routes.route("/load")
def load():
  image_list = []

  # get images
  for img in os.scandir("uploads/images"):
    if img.name.endswith(".png") or img.name.endswith(".jpg") or img.name.endswith(".jpeg"):
      image_list.append(img.path)

  response = jsonify(
      images=image_list
  )

  return response


@images_routes.route("/purchases")
def history():
  return Response(f"Looks like there are no purchases!")
