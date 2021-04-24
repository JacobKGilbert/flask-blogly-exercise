from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors real errors instead of HTML
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserRouteTestCase(TestCase):
  '''Tests for User flask routes.'''

  def setUp(self):
    User.query.delete()

    user = User(first_name='Test', last_name='Case')
    db.session.add(user)
    db.session.commit()

    self.user = user

  def tearDown(self):
    db.session.rollback()

  def test_home_rt(self):
    with app.test_client() as client:
      res = client.get('/users')
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)

  def test_user_list(self):
    with app.test_client() as client:
      res = client.get('/users')
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn( 
          f'<li><a href="/users/{self.user.id}">{self.user.first_name} {self.user.last_name}</a></li>' , html)

  def test_user_info(self):
    with app.test_client() as client:
      res = client.get(f'/users/{self.user.id}')
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn(
          f'<h2>{self.user.first_name} {self.user.last_name}</h2>', html)

  def test_edit_page(self):
    with app.test_client() as client:
      res = client.get(f'/users/{self.user.id}/edit')
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn('Save', html)

