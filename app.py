"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'hello123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_rt():
  '''Get home page.'''
  return redirect('/users')

# User Routes
@app.route('/users')
def users_list_rt():
  '''Renders all users into list.'''
  users = User.query.all()
  return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def new_user_rt():
  '''GET new user form. POST new user into database.'''
  if request.method == 'POST':
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    img_url = request.form['imgUrl'] if request.form['imgUrl'] else None
    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')
  else:
    return render_template('new_user_form.html')

@app.route('/users/<int:user_id>')
def select_user_rt(user_id):
  '''Show details for single user.'''
  user = User.query.get_or_404(user_id)
  posts = Post.query.filter_by(user_id = user_id).all()
  return render_template('user_info.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user_rt(user_id):
  '''GET edit_user form. POST edits to user into database.'''
  if request.method == 'POST':
    ed_user = User.query.get(user_id)
    ed_user.first_name = request.form['firstName']
    ed_user.last_name = request.form['lastName']
    ed_user.img_url = request.form['imgUrl'] if request.form['imgUrl'] else None

    db.session.add(ed_user)
    db.session.commit()

    return redirect('/users')
  else:
    user = User.query.get(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user_rt(user_id):
  '''Delete select user.'''
  User.query.filter(User.id == user_id).delete()
  
  db.session.commit()
  return redirect('/')

# Blog Post Routes
@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def new_post_rt(user_id):
  '''GET new post form. POST new blog post.'''
  if request.method == 'POST':
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')
  else:
    user = User.query.get(user_id)
    return render_template('new_post_form.html', user=user)

@app.route('/posts/<int:post_id>')
def select_post_rt(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post_rt(post_id):
  '''GET edit_post form. POST edits for blog post into database.'''
  if request.method == 'POST':
    ed_po = Post.query.get(post_id)
    ed_po.title = request.form['title']
    ed_po.content = request.form['content']

    db.session.add(ed_po)
    db.session.commit()

    return redirect(f'/posts/{post_id}')
  else:
    post = User.query.get(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post_rt(post_id):
  '''Delete select post.'''
  post = Post.query.get(post_id)
  user_id = post.author.id

  post.delete()

  db.session.commit()
  return redirect(f'/users/{user_id}')
