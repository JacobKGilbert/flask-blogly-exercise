from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors real errors instead of HTML
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class PostRouteTestCase(TestCase):
  '''Tests for Blog Post flask routes.'''

  def setUp(self):
    Post.query.delete()
    User.query.delete()

    user = User(first_name='Test', last_name='Case')
    db.session.add(user)
    db.session.commit()

    post = Post(title='Post Test', content='Test content.', user_id=user.id)
    db.session.add(post)
    db.session.commit()

    self.user = user
    self.post = post

  def tearDown(self):
    db.session.rollback()

  def test_new_post_form(self):
    with app.test_client() as client:
      res = client.get(f'/users/{self.user.id}/posts/new')
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn('<h1>New Post</h1>', html)

  def test_post_page(self):
    with app.test_client() as client:
      res = client.get(f'/posts/{self.post.id}')
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn(f'<h1>{self.post.title}</h1>', html)
