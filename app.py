"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
  return redirect('/users')

@app.route('/users')
def users_list_rt():
  '''Renders all users into list.'''
  return render_template('users.html')

@app.route('/users/new', methods=['GET', 'POST'])
def new_user_rt():
  '''GET new user form. POST new user into database.'''
  if request.method == 'POST':
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    img_url = request.form['imgUrl']
    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')
  else:
    return render_template('form.html')

@app.route('/users/{user_id}')
def select_user_rt(user_id):
  return render_template('user_info.html')