import json
import os
import errno

from flask import Blueprint, Response, jsonify, request, make_response

from .image_model import Image
from util.error_util import ErrorUtil

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

# RICPADILLA DELETE WHEN DONE
# TODO: USE THIS API CALL TO STORE THE DIR. IN THE DB
@images_routes.route("/AddNewDirectory", methods=['POST'])
def add_new_directory():
  # Check if data is provided in request
  if not request.data:
    return ErrorUtil.get_json_response(ErrorUtil.JSON_DATA_MISSING)
  
  # Get user id from request
  if str(request.json.get('userId')) != 'None':
    try:
      user_id = int(request.json.get('userId'))
    except:
      return ErrorUtil.get_json_response(ErrorUtil.MALFORMED_USER_ID)
  else:
    return ErrorUtil.get_json_response(ErrorUtil.NO_USER_ID)
  
  # Get directory path from request
  if str(request.json.get('dirPath')) != 'None':
    dir_path = str(request.json.get('dirPath'))
  else:
    return ErrorUtil.get_json_response(ErrorUtil.NO_DIRECTORY_PATH)
  
  # Add directory path for user in DB
  dir_id, result = Image.add_new_directory(user_id, dir_path)

  if result:
    data = {
      'status': 'New directory has been added successfully.',
      'directoryId': dir_id
    }
    return make_response(jsonify(data), 200)
  else:
    return ErrorUtil.get_json_response(ErrorUtil.FAILED_TO_ADD_DIRECTORY)
  
@images_routes.route("/albums", methods=['GET'])
def get_albums() -> str:

    albums, result = Image.get_albums()

    if result:
        return jsonify({'status': 'success', 'albums': albums})
    else:
        return ErrorUtil.get_json_response(ErrorUtil.FAILED_TO_GET_ALBUMS)
    

@images_routes.route("/albums/<id>", methods=['DELETE'])
def delete_album(id) -> str:

    album_id, result = Image.delete_album(id)

    if result:
        return jsonify({'status': 'success', 'id': album_id})
    else:
        return ErrorUtil.get_json_response(ErrorUtil.FAILED_TO_DELETE_ALBUM)
    
@images_routes.route("/GetSubDirAndFiles", methods=['POST'])
def get_subdirectories_and_files():
   # Check if data is provided in request
  if not request.data:
    return ErrorUtil.get_json_response(ErrorUtil.JSON_DATA_MISSING)
  data = request.get_json()
  if not data:
    return ErrorUtil.get_json_response(ErrorUtil.JSON_DATA_MISSING)
  
  # Get directory path from request
  if str(request.json.get('dirPath')) != 'None':
    dir_path = str(request.json.get('dirPath')).rstrip("/")
  else:
    return ErrorUtil.get_json_response(ErrorUtil.NO_DIRECTORY_PATH)
  
  # Scan given directory
  try:
     dir_entry_objects = os.scandir('/app/uploads/' + dir_path)
  except OSError as error:
     if error.errno in (errno.EACCES, errno.EPERM):
        return ErrorUtil.get_json_response(ErrorUtil.DIR_PERMISSION_DENIED)
     elif error.errno == errno.ENOENT:
        return ErrorUtil.get_json_response(ErrorUtil.DIR_NOT_FOUND)
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

     if dir_entry.is_file():
        files.append(dir_path + dir_entry.name)

  dir_entry_objects.close()

  if sub_dirs.count == 0 and files.count == 0:
     return ErrorUtil.get_json_response(ErrorUtil.DIR_IS_EMPTY)
  else:
     return jsonify({'Directories': sub_dirs, 'Files': files})
