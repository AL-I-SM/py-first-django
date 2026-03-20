from django.test import TestCase 
from classbook.models import User
from blog.models import Topic
import pytest
from django.urls import reverse
import uuid

@pytest.fixture
def test_password():
   return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)
   return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
   def make_auto_login(user=None):
        if user:
            client.logout()
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user
   return make_auto_login


@pytest.mark.django_db
def test_auth_view(auto_login_user):
   client, user = auto_login_user()
   url = reverse('topics')
   response = client.get(url)
   assert response.status_code == 200


@pytest.mark.django_db
def test_owner_view(auto_login_user):
   client, user = auto_login_user()
   Topic.objects.create(owner=user)
   topic = Topic.objects.filter(owner=user).first()
   url = reverse('topic', args=[topic.id])
   response = client.get(url)
   assert response.status_code == 200


@pytest.mark.django_db
def test_not_owner_view(auto_login_user):
   client, user = auto_login_user()
   client.login(username=user.username, password="some_passwors")
   Topic.objects.create(owner=user)
   
   client, another_user = auto_login_user()
   client.login(username=another_user.username, password="some_passwors")
   topic = Topic.objects.all().first()
   
   url = reverse('topic', args=[topic.id])
   response = client.get(url)
   assert response.status_code == 404


@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('user', 'user@mail.com', 'password', is_superuser = 'True')
  assert User.objects.count() == 1


@pytest.mark.django_db
def test_view_topic_as_admin(admin_client, auto_login_user):
   client, user = auto_login_user()
   Topic.objects.create(owner=user)
   client.logout()
   
   topic = Topic.objects.all().first()
   url = reverse('topic', args=[topic.id])
   
   response = client.get(url)
   assert response.status_code == 302

   client = admin_client
   response = client.get(url)
   assert response.status_code == 200


@pytest.mark.django_db
def test_view_topics_as_admin(admin_client):
   url = reverse('topics')
   response = admin_client.get(url)
   assert response.status_code == 200


@pytest.mark.django_db
def test_view_unauthorized(client):
   url = reverse('topics')
   response = client.get(url)
   assert response.status_code == 302


class TopcisCreationTests(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create(username = 'test_user1', first_name='fist_name_1')
        self.user2 = User.objects.create(username = 'test_user2', first_name='fist_name_2')
        self.superuser = User.objects.create(username = 'test_superuser', first_name='superuser', is_superuser="True")

    def test_add_topics(self):
        Topic.objects.create(text='text1', owner=self.user1)
        Topic.objects.create(text='text2', owner=self.user2)
        get_data=Topic.objects.all()
        assert len(get_data) == 2
        assert get_data.filter(owner=self.user1)[0].text == "text1"
        assert get_data.filter(owner=self.user2)[0].text == "text2"
        # self.assertEquals(len(get_data), 2)
        # self.assertEquals(get_data.filter(owner=self.user1)[0].text, "text1")
        # self.assertEquals(get_data.filter(owner=self.user2)[0].text, "text2")

    def test_read_topics_by_superuser(self):
        pass

    def test_read_topic_by_different_users(self):
        pass

# pytest --cov-report html --cov=app_test
# pytest --cov=app_test
# pytest -v

# coverage run --source='.' ..\manage.py test tests 
# coverage report
# coverage html    