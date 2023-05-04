from flask import Blueprint, Response, jsonify, request
from .tagging_model import Taging
tagging_routes = Blueprint("tagging_routes", __name__, url_prefix="/tagging")


@tagging_routes.route('/tag-all-images', methods=['POST'])
def tag_all_images():
  # check
  if not request.data:
    return jsonify({'request': 'No JSON data provided'}), 400

  if request.json.get('dir_id') == None:
    return jsonify({'request': 'No dir_id is provided'}), 400

  dir_id = request.json.get('dir_id')

  if request.json.get('tags') == None and len(request.json.get('tags')) == 0:
    return jsonify({'request': 'No tags are provided'}), 400

  tags = request.json.get('tags')

  temp_tag_ids = Taging.tag_all_images(dir_id, tags)

  return jsonify({'tag_ids:': temp_tag_ids}), 200


@tagging_routes.route('/tag-image', methods=['POST'])
def tag_image():
  if not request.data:
    return jsonify({'request': 'No JSON data provided'}), 404

  if request.json.get('dir_id') == None:
    return jsonify({'request': 'No dir_id is provided'}), 400

  dir_id = request.json.get('dir_id')

  if str(request.json.get('photo_id') != 'None'):
    try:
      photo_id = int(request.json.get('photo_id'))
    except:
      return jsonify({'error': 'Photo ID is of incorrect type'}), 404
  else:
    return jsonify({'error:': 'Photo ID not provided'})

  if request.json.get('tags') == None and len(request.json.get('tags')) == 0:
    return jsonify({'request': 'No tags are provided'}), 400

  tags = request.json.get('tags')

  # temp_tag_ids = Taging.tag_image(photo_id, tags)
  temp_tag_ids = Taging.tag_all_images(dir_id, tags, photo_id)

  return jsonify({'tag_ids:': temp_tag_ids}), 200
  # if str(request.json.get('photo_id') != None):
  #     try:
  #         img_id = int(request.json.get('photo_id'))
  #     except:
  #         return jsonify({'error': 'photo ID is of incorrect type'}),400
  # else:
  #     return jsonify({'error:': 'image id not provided' }),400
  # #check and get tag ID

  # if str(request.json.get('tag_id') != 'None'):
  #     try:
  #         tag_id = int(request.json.get('tag_id'))
  #     except:
  #         return jsonify({'error': 'ID is of incorrect type'}),400
  # else:
  #     return jsonify({'error:': 'tag id not provieded' }),400

  img_tag = Taging.add_tags(tag_id, img_id)

  # if img_tag:
  #     return f"Image: {img_id} tagged with tag: {tag_id}"
  # else:
  #     return f"Image: {img_id} failed to be tagged with tag: {tag_id}"

# Func to tag all images in a directory


@tagging_routes.route('/tag-images', methods=['POST'])
def tag_all_images_dir():
  # check
  if not request.data:
    return jsonify({'request': 'No JSON data provided'}), 404
  # check and get image ID
  if str(request.json.get('id') != 'None'):
    try:
      dir_id = int(request.json.get('id'))
    except:
      return jsonify({'error': 'Directory ID is of incorrect type'}), 404
  else:
    return jsonify({'error:': 'Directory id not provided'}), 404

  # check and get tag ID
  if str(request.json.get('tag_id') != 'None'):
    try:
      tag_id = int(request.json.get('tag_id'))
    except:
      return jsonify({'error': 'Tag ID is of incorrect type'}), 404
  else:
    return jsonify({'error:': 'Tag id not provieded'}), 404

  img_tag = Taging.add_bulk_tags_to_dir(tag_id, dir_id)

  if img_tag:
    return f"Image in directory: {dir_id} tagged with tag: {tag_id}"
  else:
    return f"Images in directory: {dir_id} failed to be tagged with tag: {tag_id}"


# delete tags
@tagging_routes.route('/delete-tag', methods=['DELETE'])
def delete_tag():
    # check
  if not request.data:
    return jsonify({'request': 'No JSON data provided'}), 400
  # check and get image ID
  if str(request.json.get('photo_id') != 'None'):
    try:
      photo_id = int(request.json.get('photo_id'))
    except:
      return jsonify({'error': 'ID is of incorrect type'}), 400
  else:
    return jsonify({'error:': 'Photo ID id not provided'}), 400

  # check and get tag ID
  if str(request.json.get('tag_id') != 'None'):
    try:
      tag_id = int(request.json.get('tag_id'))
    except:
      return jsonify({'error': 'ID is of incorrect type'}), 40
  else:
    return jsonify({'error:': 'Tag id not provided'}), 400

  img_tag = Taging.delete_tags(tag_id, photo_id)

  if img_tag == True:
    return jsonify({"msg": f"Tag: {tag_id} was removed from Photo: {photo_id} "})
  else:
    return jsonify({"msg": f"Tag: {tag_id} failed to be removed from photo: {photo_id}"})
