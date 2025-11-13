import os
from supabase.client import create_client, Client

class SupabaseClient:
  _instance = None

  def __init__(self):
    if SupabaseClient._instance is not None:
      return SupabaseClient._instance

    self.supabase_url = os.environ.get('SUPABASE_URL')
    self.supabase_key = os.environ.get('SUPABASE_KEY')

    if not self.supabase_url or not self.supabase_key:
        raise ValueError("Supabase credentials missing")

    self._client = create_client(self.supabase_url, self.supabase_key)
    SupabaseClient._instance = self

  @property
  def client(self) -> Client:
      return self._client

  def get_posts(self):
    try:
      response = self.client.table('posts').select('*').execute()
      return response.data
    except Exception as e:
      print(f"Error fetching posts: {e}")
      return []

  def create_post(self, title, content, author_id, author_name):
    try:
      response = self.client.table('posts').insert({
        'title': title,
        'content': content,
        'author_id': author_id,
        'author_name': author_name
      }).execute()
      return response.data[0] if response.data else None
    except Exception as e:
      print(f"Error creating post: {e}")
      return None

  def get_post(self, post_id):
    try:
      response = self.client.table('posts').select('*').eq('id', post_id).execute()
      return response.data[0] if response.data else None
    except Exception as e:
      print(f"Error fetching post: {e}")
      return None

  def update_post(self, post_id, title, content):
    try:
      response = self.client.table('posts').update({
        'title': title,
        'content': content
      }).eq('id', post_id).execute()
      return response.data[0] if response.data else None
    except Exception as e:
      print(f"Error updating post: {e}")
      return None

  def delete_post(self, post_id):
    try:
      self.client.table('comments').delete().eq('post_id', post_id).execute()

      response = self.client.table('posts').delete().eq('id', post_id).execute()
      return response.data[0] if response.data else None
    except Exception as e:
      print(f"Error deleting post: {e}")
      return None

  def create_comment(self, post_id, content, author_id, author_name):
    try:
      response = self.client.table('comments').insert({
        'post_id': post_id,
        'content': content,
        'author_id': author_id,
        'author_name': author_name
      }).execute()
      return response.data[0] if response.data else None
    except Exception as e:
      print(f"Error creating comment: {e}")
      return None

  def get_comments(self, post_id):
    try:
      response = self.client.table('comments').select('*').eq('post_id', post_id).execute()
      return response.data
    except Exception as e:
      print(f"Error fetching comments: {e}")
      return []

supabase_client = SupabaseClient()
