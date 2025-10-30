import os
from dotenv import load_dotenv

load_dotenv()

from app.model import supabase_client

print("Testing Supabase connection...")

try:
  client = supabase_client.client
  print("Supabase client connected successfully")
except Exception as e:
  print(f"Connection failed: {e}")
