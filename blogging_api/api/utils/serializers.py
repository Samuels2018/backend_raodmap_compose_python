
def serialize_post(post):
  if not post:
    return None
  post['_id'] = str(post['_id'])
  return post