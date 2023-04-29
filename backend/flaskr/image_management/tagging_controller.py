from flask import Blueprint, Response, jsonify, request
from tagging_model import Taging
images_routes = Blueprint("images_routes", __name__, url_prefix="/images")


@images_routes.route('/taged', methods= ['POST'])

# add tags
def tag_image():
    #check
    if not request.data:
        return jsonify({'request': 'No JSON data provided'}), 404
    #check and get image ID
    if str(request.json.get('photo_id') != 'None'):
        try:
            img_id = int(request.json.get('photo_id'))
        except:
            return jsonify({'error': 'ID is of incorrect type'}),404
    else:
        return jsonify({'error:': 'image id not provided' }),404
    #check and get tag ID
       
    if str(request.json.get('tag_id') != 'None'):
        try:
            tag_id = int(request.json.get('tag_id'))
        except:
            return jsonify({'error': 'ID is of incorrect type'}),404
    else:
        return jsonify({'error:': 'image id not provieded' }),404
    
    img_tag = Taging.add_tags(tag_id, img_id)
    
    if img_tag:
        return f"Image: {img_id} tagged with tag: {tag_id}"
    else:
        return f"Image: {img_id} failed to be tagged with tag: {tag_id}"

# Func to tag all images in a directory
def tag_all_images_dir():
    #check
    if not request.data:
        return jsonify({'request': 'No JSON data provided'}), 404
    #check and get image ID
    if str(request.json.get('id') != 'None'):
        try:
            dir_id = int(request.json.get('id'))
        except:
            return jsonify({'error': 'ID is of incorrect type'}),404
    else:
        return jsonify({'error:': 'Directory id not provided' }),404
    
    #check and get tag ID
    if str(request.json.get('tag_id') != 'None'):
        try:
            tag_id = int(request.json.get('tag_id'))
        except:
            return jsonify({'error': 'ID is of incorrect type'}),404
    else:
        return jsonify({'error:': 'Tag id not provieded' }),404
    
    img_tag = Taging.add_bulk_tags_to_dir(tag_id, dir_id)
    
    if img_tag:
        return f"Image in directory: {dir_id} tagged with tag: {tag_id}"
    else:
        return f"Images in directory: {dir_id} failed to be tagged with tag: {tag_id}"




# delete tags
def delete_tag():
     #check
    if not request.data:
        return jsonify({'request': 'No JSON data provided'}), 404
    #check and get image ID
    if str(request.json.get('photo_id') != 'None'):
        try:
            photo_id = int(request.json.get('photo_id'))
        except:
            return jsonify({'error': 'ID is of incorrect type'}),404
    else:
        return jsonify({'error:': 'Photo ID id not provided' }),404
    
    #check and get tag ID
    if str(request.json.get('tag_id') != 'None'):
        try:
            tag_id = int(request.json.get('tag_id'))
        except:
            return jsonify({'error': 'ID is of incorrect type'}),404
    else:
        return jsonify({'error:': 'Tag id not provieded' }),404
    
    img_tag = Taging.delete_tags(tag_id, photo_id)
    
    if img_tag:
        return f"Image in directory: {photo_id} tagged with tag: {tag_id}"
    else:
        return f"Images in directory: {photo_id} failed to be tagged with tag: {tag_id}"

