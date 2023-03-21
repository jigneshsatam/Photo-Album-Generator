import json

from flask import Blueprint, Response, jsonify

from .image_model import Image

images_routes = Blueprint("images_routes", __name__, url_prefix="/images")


@images_routes.route("/load")
def load() -> str:

  images = Image.get_images("uploads/images")

  response = {
      "images": [img.__dict__ for img in images]
  }

  return json.dumps(response)


@images_routes.route("/purchases")
def history():
  return Response(f"Looks like there are no purchases!")
