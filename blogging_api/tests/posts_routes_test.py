import unittest
from flask import Flask
from flask.testing import FlaskClient
from api.models.post import Post
from api.extensions import mongo as db
from api import create_app
from api.config import Config

class PostRoutesTestCase(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    # Configurar aplicación de prueba
    class TestConfig(Config):
      MONGO_URI = "mongodb://localhost:27017"
      MONGO_DBNAME = "test_db"
    
    cls.app = create_app(TestConfig)
    cls.client = cls.app.test_client()
    cls.app_context = cls.app.app_context()
    cls.app_context.push()

  @classmethod
  def tearDownClass(cls):
    # Limpiar base de datos después de las pruebas
    if hasattr(db, 'cx') and db.cx:
      db.cx.drop_database("test_db")  # Usar el mismo nombre que en setUp
    cls.app_context.pop()
    if hasattr(db, 'cx') and db.cx:
      db.cx.close()

  def setUp(self):
    # Datos de prueba
    self.test_post_data = {
      'title': 'Test Post',
      'content': 'This is a test post content',
      'category': 'technology'
    }
    
    # Insertar documento de prueba
    if not hasattr(db, 'db') or db.db is None:
      self.skipTest("MongoDB connection not available")
        
    result = db.db.posts.insert_one(self.test_post_data.copy())
    self.test_post_id = str(result.inserted_id)

  def tearDown(self):
    if hasattr(db, 'db') and db.db is not None:
      db.db.posts.drop()
  # Tests para GET /posts
  def test_get_posts(self):
    response = self.client.get('/api/v1/posts')
    self.assertEqual(response.status_code, 200)
    self.assertIsInstance(response.json, list)
    self.assertGreater(len(response.json), 0)

  def test_get_posts_with_search_term(self):
    response = self.client.get('/api/v1/posts?term=Test')
    self.assertEqual(response.status_code, 200)
    self.assertIsInstance(response.json, list)
    self.assertGreater(len(response.json), 0)

  # Tests para POST /posts/create
  def test_create_post_success(self):
    response = self.client.post(
      '/api/v1/posts/create',
      json=self.test_post_data
    )
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['title'], self.test_post_data['title'])

  def test_create_post_missing_fields(self):
    invalid_data = {'title': 'Missing Fields'}
    response = self.client.post(
      '/api/v1/posts/create',
      json=invalid_data
    )
    self.assertEqual(response.status_code, 400)
    self.assertIn('error', response.json)

  # Tests para GET /posts/<post_id>
  def test_get_post_success(self):
    response = self.client.get(f'/api/v1/posts/{self.test_post_id}')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['id'], self.test_post_id)

  def test_get_post_not_found(self):
    response = self.client.get('/api/v1/posts/nonexistent_id')
    self.assertEqual(response.status_code, 404)
    self.assertIn('error', response.json)

  # Tests para PUT /posts/<post_id>
  def test_update_post_success(self):
    updated_data = {
      'title': 'Updated Title',
      'content': 'Updated content',
      'category': 'science'
    }
    response = self.client.put(
      f'/api/v1/posts/{self.test_post_id}',
      json=updated_data
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['title'], updated_data['title'])

  def test_update_post_not_found(self):
    response = self.client.put(
      '/api/v1/posts/nonexistent_id',
      json=self.test_post_data
    )
    self.assertEqual(response.status_code, 404)
    self.assertIn('error', response.json)

  # Tests para DELETE /posts/<post_id>
  def test_delete_post_success(self):
    response = self.client.delete(f'/api/v1/posts/{self.test_post_id}')
    self.assertEqual(response.status_code, 204)

  def test_delete_post_not_found(self):
    response = self.client.delete('/api/v1/posts/nonexistent_id')
    self.assertEqual(response.status_code, 404)
    self.assertIn('error', response.json)

if __name__ == '__main__':
  unittest.main()