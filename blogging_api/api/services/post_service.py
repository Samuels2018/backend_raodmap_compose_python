from api.models.post import Post
from flask import jsonify

class PostService:
  @staticmethod
  def get_all_posts(search_term=None):
    if search_term:
      posts = Post.search(search_term)
    else:
      posts = Post.get_all()
    return [PostService._serialize_post(post) for post in posts]
  
  @staticmethod
  def get_post(post_id):
    post = Post.get_by_id(post_id)
    if not post:
      return None
    return PostService._serialize_post(post)
  
  @staticmethod
  def create_post(data):
    required_fields = ['title', 'content', 'category']
    if not all(field in data for field in required_fields):
      return None
        
    return Post.create(data)
  
  @staticmethod
  def update_post(post_id, data):
    required_fields = ['title', 'content', 'category']
    if not all(field in data for field in required_fields):
      return None
        
    return Post.update(post_id, data)
  
  @staticmethod
  def delete_post(post_id):
    return Post.delete(post_id)
  
  @staticmethod
  def _serialize_post(post):
    if not post:
      return None
    post['_id'] = str(post['_id'])
    return post