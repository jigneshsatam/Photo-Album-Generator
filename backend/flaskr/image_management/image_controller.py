import json

from flask import Blueprint, Response, jsonify, request

from .image_model import Image

images_routes = Blueprint("images_routes", __name__, url_prefix="/images")


@images_routes.route("/load", methods=['GET'])
def load() -> str:

  directory = request.args.to_dict().get("directory")

  images = Image.get_images(directory)

  response = {
      "images": [img.__dict__ for img in images]
  }

  return json.dumps(response)


@images_routes.route("/purchases")
def history():
  return Response(f"Looks like there are no purchases!")
