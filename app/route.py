import datetime
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.model import supabase_client
from datetime import timedelta

main = Blueprint('main', __name__)

ADMIN_USERS = ['daniel']

def is_admin():
  return session.get('username') in ADMIN_USERS

@main.app_template_filter('format_time')
def format_time(date_value):
  if not date_value:
    return 'Now'

  try:
    if isinstance(date_value, str):
      date_part = date_value.split('T')[0]
      time_part = date_value.split('T')[1][:5]

      year, month, day = date_part.split('-')
      hour = time_part.split(':')[0]
      minute = time_part.split(':')[1]

      return f"{year}/{month}/{day} {hour}:{minute}"
  except:
    pass

  return 'Now'

@main.route('/')
def index():
  posts = supabase_client.get_posts()
  return render_template('index.htm', posts=posts)

@main.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    session['user_id'] = str(uuid.uuid4())
    session['username'] = username
    session['is_admin'] = username in ADMIN_USERS
    flash('Logged in', 'success')
    return redirect(url_for('main.index'))
  return render_template('login.htm')

@main.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username')
    session['user_id'] = str(uuid.uuid4())
    session['username'] = username
    session['is_admin'] = username in ADMIN_USERS
    flash('Account created!', 'success')
    return redirect(url_for('main.index'))
  return render_template('register.htm')

@main.route('/logout')
def logout():
  session.clear()
  flash('Logged out!', 'success')
  return redirect(url_for('main.index'))

@main.route('/create', methods=['GET', 'POST'])
def create_post():
  if 'user_id' not in session:
    flash('Log in to create post', 'error')
    return redirect(url_for('main.login'))

  if request.method == 'POST':
    title = request.form.get('title')
    content = request.form.get('content')

    if title and content:
      post = supabase_client.create_post(
        title=title,
        content=content,
        author_id=session['user_id'],
        author_name=session['username']
      )
      if post:
        flash('Post created', 'success')
        return redirect(url_for('main.index'))
      else:
        flash('Error creating post', 'error')

  return render_template('create_post.htm')

@main.route('/post/<post_id>', methods=['GET', 'POST'])
def view_post(post_id):
  if request.method == 'POST':
    if 'user_id' not in session:
      flash('Log in to comment', 'error')
      return redirect(url_for('main.login'))

    content = request.form.get('content')
    if content:
      comment = supabase_client.create_comment(
        post_id=post_id,
        content=content,
        author_id=session['user_id'],
        author_name=session['username']
      )
      if comment:
        flash('Comment added', 'success')
      else:
        flash('Error adding comment', 'error')

  post = supabase_client.get_post(post_id)
  comments = supabase_client.get_comments(post_id)

  if not post:
    flash('Post not found', 'error')
    return redirect(url_for('main.index'))

  return render_template('post.htm', post=post, comments=comments)

@main.route('/post/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
  if 'user_id' not in session:
    flash('Log in to delete post', 'error')
    return redirect(url_for('main.login'))

  if not session.get('is_admin'):
    flash('Only admin users can delete posts', 'error')
    return redirect(url_for('main.view_post', post_id=post_id))

  post = supabase_client.get_post(post_id)
  if not post:
    flash('Post not found', 'error')
    return redirect(url_for('main.index'))

  result = supabase_client.delete_post(post_id)
  if result:
    flash('Post deleted', 'success')
  else:
    flash('Error deleting post', 'error')

  return redirect(url_for('main.index'))

@main.route('/profile')
def profile():
  if 'user_id' not in session:
    flash('Log in to view profile', 'error')
    return redirect(url_for('main.login'))
  return render_template('profile.htm', user=session)
