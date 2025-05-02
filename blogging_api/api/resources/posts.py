from flask import Blueprint, request, jsonify
from api.services.post_service import PostService
from api.utils.decorators import validate_json

posts_bp = Blueprint('posts', __name__, url_prefix='/api/v1')

@posts_bp.route('/posts', methods=['GET'])
def get_posts():
  search_term = request.args.get('term')
  posts = PostService.get_all_posts(search_term)
  return jsonify(posts), 200

@posts_bp.route('/posts/create', methods=['POST'])
@validate_json(['title', 'content', 'category'])
def create_post():
  data = request.get_json()
  post = PostService.create_post(data)
  if not post:
    return jsonify({'error': 'Failed to create post'}), 400
  return jsonify(post), 201

@posts_bp.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
  post = PostService.get_post(post_id)
  if not post:
    return jsonify({'error': 'Post not found'}), 404
  return jsonify(post), 200

@posts_bp.route('/posts/<post_id>', methods=['PUT'])
@validate_json(['title', 'content', 'category'])
def update_post(post_id):
  data = request.get_json()
  post = PostService.update_post(post_id, data)
  if not post:
    return jsonify({'error': 'Post not found or invalid data'}), 404
  return jsonify(post), 200

@posts_bp.route('/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
  if not PostService.delete_post(post_id):
    return jsonify({'error': 'Post not found'}), 404
  return '', 204