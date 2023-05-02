import json
import os
import errno

from flask import Blueprint, Response, jsonify, request, make_response

from .image_model import Image

images_routes = Blueprint("images_routes", __name__, url_prefix="/images")


@images_routes.route("<int:dir_id>/load", methods=['GET'])
def load(dir_id) -> str:

  directory = request.args.to_dict().get("directory")
  directory, result = Image.get_dir_path(dir_id)
  images = []
  if result == True:
    images = Image.get_images("uploads/" + directory)

    response = {
        "images": [img.__dict__ for img in images]
    }

    return json.dumps(response)

  return json.dumps({}), 404


@images_routes.route("/purchases")
def history():
  return Response(f"Looks like there are no purchases!")

# RICPADILLA DELETE WHEN DONE
# TODO: USE THIS API CALL TO STORE THE DIR. IN THE DB


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
    data = {
        'status': 'New directory has been added successfully.',
        'directoryId': dir_id
    }
    return make_response(jsonify(data), 200)
  else:
    return jsonify({'status': 'Fail! New directory has not been added.'}), 500


@images_routes.route("/albums", methods=['GET'])
def get_albums() -> str:

  albums, result = Image.get_albums()

  if result:
    return jsonify({'status': 'success', 'albums': albums})
  else:
    return jsonify({'status': 'fail'}), 500


@images_routes.route("/albums/<id>", methods=['DELETE'])
def delete_album(id) -> str:

  album_id, result = Image.delete_album(id)

  if result:
    return jsonify({'status': 'success', 'id': album_id})
  else:
    return jsonify({'status': 'fail'}), 500


@images_routes.route("/GetSubDirAndFiles", methods=['POST'])
def get_subdirectories_and_files():
   # Check if data is provided in request
  data = request.get_json()
  if not data:
    return jsonify({'status': 'JSON data is missing'}), 404

  # Get directory path from request
  if str(request.json.get('dirPath')) != 'None':
    dir_path = str(request.json.get('dirPath')).rstrip("/")
  else:
    return jsonify({"status": 'directory path is missing'}), 404

  # Scan given directory
  try:
    dir_entry_objects = os.scandir('/app/uploads/' + dir_path)
  except OSError as error:
    if error.errno in (errno.EACCES, errno.EPERM):
      return jsonify({"status": 'permission denied when accessing directory'}), 401
    elif error.errno == errno.ENOENT:
      return jsonify({"status": 'directory not found'}), 404
    else:
      return jsonify({"status": error}), 500

  # Get contents in given directory
  sub_dirs = []
  files = []
  if dir_path != "":
    dir_path = dir_path + '/'
  for dir_entry in dir_entry_objects:
    if dir_entry.is_dir():
      sub_dirs.append(dir_path + dir_entry.name)

    #  if dir_entry.is_file():
    #     files.append(dir_path + dir_entry.name)

  dir_entry_objects.close()

  if sub_dirs.count == 0 and files.count == 0:
    return jsonify({'status': 'No subdirectories or files found in given directory.'})
  else:
    return jsonify({'Directories': sub_dirs, 'Files': files})


@images_routes.route("/FetchImagesFromTags", methods=['POST'])
def fetch_images_from_tags():
  # Check if data is provided in request
  if not request.data:
    return jsonify({'status': 'JSON data is missing'}), 404

  # Get user id from request
  if str(request.json.get('userId')) != 'None':
    try:
      user_id = int(request.json.get('userId'))
    except:
      return jsonify({'status': 'given user id is not an integer'}), 400
  else:
    return jsonify({'status': 'user id is missing'}), 404

  # Get tag list from request
  if str(request.json.get('tags')) == 'None':
    return jsonify({"status": 'tag list is missing'}), 404
  request_data = json.loads(request.data)
  tag_list = []
  for tag in request_data["tags"]:
    tag_list.append(str(tag))

  # Get images from tag list
  result_imgs = Image.get_images_from_tags(user_id, tag_list)

  return jsonify({"images": result_imgs})
