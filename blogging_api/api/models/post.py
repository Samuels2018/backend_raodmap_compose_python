from datetime import datetime
from bson import ObjectId
from api.extensions import mongo

class Post:
  @staticmethod
  def get_all():
    return list(mongo.db.posts.find())
    
  @staticmethod
  def get_by_id(post_id):
    if not ObjectId.is_valid(post_id):
      return None
    return mongo.db.posts.find_one({'_id': ObjectId(post_id)})
    
  @staticmethod
  def create(data):
    print(f"Accessing collection: {mongo.db}")
    post = {
      'title': data['title'],
      'content': data['content'],
      'category': data['category'],
      'tags': data.get('tags', []),
      'createdAt': datetime.utcnow(),
      'updatedAt': datetime.utcnow()
    }
    result = mongo.db.posts.insert_one(post)
    post['_id'] = str(result.inserted_id)
    return post
  
  @staticmethod
  def update(post_id, data):
    if not ObjectId.is_valid(post_id):
      return None
        
    updated_data = {
      'title': data['title'],
      'content': data['content'],
      'category': data['category'],
      'tags': data.get('tags', []),
      'updatedAt': datetime.utcnow()
    }
    
    result = mongo.db.posts.update_one(
      {'_id': ObjectId(post_id)},
      {'$set': updated_data}
    )
    
    if result.modified_count == 0:
      return None
        
    updated_post = mongo.db.posts.find_one({'_id': ObjectId(post_id)})
    updated_post['_id'] = str(updated_post['_id'])
    return updated_post
  
  @staticmethod
  def delete(post_id):
    if not ObjectId.is_valid(post_id):
      return False
    result = mongo.db.posts.delete_one({'_id': ObjectId(post_id)})
    return result.deleted_count > 0
  
  @staticmethod
  def search(term):
    query = {
      '$or': [
        {'title': {'$regex': term, '$options': 'i'}},
        {'content': {'$regex': term, '$options': 'i'}},
        {'category': {'$regex': term, '$options': 'i'}}
      ]
    }
    return list(mongo.db.posts.find(query))