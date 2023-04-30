from flask import Blueprint, Response, jsonify, request
from .tag_model import Tag

tag_routes = Blueprint("tag_routes", __name__, url_prefix="/tags")

# Register User call
@tag_routes.route("/addTags", methods=['POST'])
def create_tag():
    # Create Tag in DB
    tag_id, result = Tag.create_tag((request.json.get('tags')))

    if result:
        return jsonify({'status': 'Tag has been Created',
                         'tagId': tag_id})
    else:
        return jsonify({'status': 'Tag creation failed'}), 500


@tag_routes.route("/fetchTags", methods=['GET'])
def get_tags() -> str:

    tags, result = Tag.get_tags()

    if result:
        return jsonify({'status': 'success', 'tags': tags})
    else:
        return jsonify({'status': 'fail'}), 500