"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):
  '''User Model'''
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  first_name = db.Column(db.String(20), nullable=False)

  last_name = db.Column(db.String(20), nullable=False)

  img_url = db.Column(db.Text, default='https://avatars.githubusercontent.com/u/76506172?s=60&v=4')

  def __repr__(self):
    u = self
    return f'<User id={u.id} first_name={u.first_name} last_name={u.last_name}>'

class Post(db.Model):
  '''Post Model'''
  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  title = db.Column(db.Text, nullable=False)

  content = db.Column(db.Text, nullable=False)

  created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))

  author = db.relationship('User', backref='posts')

  tags = db.relationship('Tag', secondary='posts_tags', backref='posts')
  
  def __repr__(self):
    p = self
    return f'<Post id={p.id} title={p.title} author={p.users.first_name} {p.users.last_name}>'

class Tag(db.Model):
  '''Tag Model'''
  __tablename__ = 'tags'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  
  tag_name = db.Column(db.Text, nullable=False, unique=True)

  def __repr__(self):
    t = self
    return f'<Tag id={t.id} tag_name={t.tag_name}>'

class PostTag(db.Model):
  '''Post Tag Join Table'''
  __tablename__ = 'posts_tags'

  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, nullable=False)

  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)
