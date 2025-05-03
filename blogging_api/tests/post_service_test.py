import unittest
from datetime import datetime
from api.services.post_service import PostService
from api.models.post import Post
from api.extensions import mongo as db
from api import create_app
from api.config import Config
from datetime import timezone

class TestPostService(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    # Configurar aplicación de prueba
    class TestConfig(Config):
      MONGO_URI = Config.MONGO_URI
      MONGO_DBNAME = Config.mongo_db
    
    cls.app = create_app(TestConfig)
    cls.app_context = cls.app.app_context()
    cls.app_context.push()

  @classmethod
  def tearDownClass(cls):
    # Limpiar base de datos después de las pruebas
    if hasattr(db, 'cx') and db.cx:  # Verifica que la conexión existe
      db.cx.drop_database(Config.mongo_db)
    cls.app_context.pop()
    # Cerrar conexión de MongoDB
    if hasattr(db, 'cx') and db.cx:
      db.cx.close()
  
  def setUp(self):
    # Datos de prueba
    self.post1 = {
      'title': 'First Post',
      'content': 'Content for first post',
      'category': 'technology',
      'created_at': datetime.now(timezone.utc)  # Usa timezone-aware datetime
    }

    
    self.post2 = {
      'title': 'Second Post',
      'content': 'Content for second post',
      'category': 'science',
      'created_at': datetime.now(timezone.utc)
    }
    if not hasattr(db, 'db') or db.db is None:
      self.skipTest("MongoDB connection not available")
    db.db.posts.insert_many([self.post1, self.post2])

  def tearDown(self):
    # Limpiar la base de datos después de cada test
    if hasattr(db, 'db') and db.db is not None:
      db.db.posts.drop()
    
  # Tests para get_all_posts
  def test_get_all_posts(self):
    posts = PostService.get_all_posts()
    self.assertEqual(len(posts), 2)
    self.assertEqual(posts[0]['title'], 'First Post')
    self.assertEqual(posts[1]['title'], 'Second Post')

  def test_get_all_posts_with_search_term(self):
    posts = PostService.get_all_posts(search_term='Second')
    self.assertEqual(len(posts), 1)
    self.assertEqual(posts[0]['title'], 'Second Post')

  # Tests para get_post
  def test_get_post_existing(self):
    post_id = str(self.post1.id)
    post = PostService.get_post(post_id)
    self.assertEqual(post['title'], 'First Post')
    self.assertEqual(post['content'], 'Content for first post')

  def test_get_post_non_existing(self):
    post = PostService.get_post('nonexistent_id')
    self.assertIsNone(post)

  # Tests para create_post
  def test_create_post_success(self):
    new_post_data = {
      'title': 'New Post',
      'content': 'New content',
      'category': 'science'
    }
    post = PostService.create_post(new_post_data)
    self.assertIsNotNone(post)
    self.assertEqual(post['title'], 'New Post')
    
    # Verificar que realmente se guardó en la base de datos
    db_post = Post.query.filter_by(title='New Post').first()
    self.assertIsNotNone(db_post)

  def test_create_post_missing_fields(self):
    invalid_data = {'title': 'Missing Fields'}
    post = PostService.create_post(invalid_data)
    self.assertIsNone(post)

  # Tests para update_post
  def test_update_post_success(self):
    post_id = str(self.post1.id)
    updated_data = {
      'title': 'Updated Title',
      'content': 'Updated content',
      'category': 'science'
    }
    post = PostService.update_post(post_id, updated_data)
    self.assertIsNotNone(post)
    self.assertEqual(post['title'], 'Updated Title')
    
    # Verificar que realmente se actualizó en la base de datos
    db_post = Post.query.get(self.post1.id)
    self.assertEqual(db_post.title, 'Updated Title')

  def test_update_post_non_existing(self):
    updated_data = {
      'title': 'Updated Title',
      'content': 'Updated content',
      'category': 'science'
    }
    post = PostService.update_post('nonexistent_id', updated_data)
    self.assertIsNone(post)

  def test_update_post_missing_fields(self):
    post_id = str(self.post1.id)
    invalid_data = {'title': 'Missing Fields'}
    post = PostService.update_post(post_id, invalid_data)
    self.assertIsNone(post)

  # Tests para delete_post
  def test_delete_post_success(self):
    post_id = str(self.post1.id)
    result = PostService.delete_post(post_id)
    self.assertTrue(result)
    
    # Verificar que realmente se eliminó de la base de datos
    db_post = Post.query.get(self.post1.id)
    self.assertIsNone(db_post)

  def test_delete_post_non_existing(self):
    result = PostService.delete_post('nonexistent_id')
    self.assertFalse(result)

  # Tests para _serialize_post
  def test_serialize_post(self):
    serialized = PostService._serialize_post({
      '_id': '507f1f77bcf86cd799439011',
      'title': 'Test',
      'content': 'Content',
      'category': 'tech'
    })
    self.assertEqual(serialized['_id'], '507f1f77bcf86cd799439011')
    self.assertEqual(serialized['title'], 'Test')

  def test_serialize_none(self):
    serialized = PostService._serialize_post(None)
    self.assertIsNone(serialized)

if __name__ == '__main__':
  unittest.main()