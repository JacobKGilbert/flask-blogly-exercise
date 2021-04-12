"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):
  '''User Model'''
  __table__ = 'users'

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  first_name = db.Column(db.String(20), nullable = False)
  last_name = db.Column(db.String(20), nullable = False)
  img_url = db.Column(db.String(), default = https://avatars.githubusercontent.com/u/76506172?s=60&v=4)
