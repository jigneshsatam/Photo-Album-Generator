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

@images_routes.route("/AddNewDirectory", methods=['POST'])
def add_new_directory():
  # Check if data is provided in request
  if not request.data:
    return jsonify({'status': 'JSON data is missing'}), 404
  
  # Get user id from request
  if str(request.json.get('userId')) != 'None':
    try:
      user_id = int(request.json.get('userId'))
    except:
      return jsonify({'status': 'given user id is not an integer'}), 404
  else:
    return jsonify({'status': 'user id is missing'}), 404
  
  # Get directory path from request
  if str(request.json.get('dirPath')) != 'None':
    dir_path = str(request.json.get('dirPath'))
  else:
    return jsonify({"status": 'directory path is missing'}), 404
  
  # Add directory path for user in DB
  dir_id, result = Image.add_new_directory(user_id, dir_path)

  if result:
    return jsonify({'status': 'New directory has been added successfully.', 'directoryId': dir_id})
  else:
    return jsonify({'status': 'Fail! New directory has not been added.'}), 500