"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):
  '''User Model'''
  __tablename__ = 'users'

  def __repr__(self):
    u = self
    return f'<User id={user_id} first_name={first_name} last_name={last_name}>'

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)

  first_name = db.Column(db.String(20), nullable = False)

  last_name = db.Column(db.String(20), nullable = False)

  img_url = db.Column(db.String(100), default = 'https://avatars.githubusercontent.com/u/76506172?s=60&v=4')

  def edit_user(self, first_name, last_name, img_url):
