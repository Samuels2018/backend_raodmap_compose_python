from functools import wraps
from flask import request, jsonify

def validate_json(required_fields):
  def decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      data = request.get_json()
      if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
      for field in required_fields:
        if field not in data:
          return jsonify({'error': f'Missing required field: {field}'}), 400
      return f(*args, **kwargs)
    return wrapper
  return decorator