from django.test import TestCase 
from classbook.models import User
from app_test.models import Topic
import pytest
from django.urls import reverse
import uuid
from serializers import ClassesSerializer

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


from classbook.models import Classes
import json


@pytest.mark.django_db
def test_Classes_API_create(admin_client):
  assert Classes.objects.count() == 0
  url = reverse('classes-list')
  data = {'name': "test1"}
  json_data = json.dumps(data)
  response = admin_client.post(url, data=json_data, content_type="application/json")
  assert response.status_code == 201
  assert Classes.objects.count() == 1
  assert Classes.objects.first().name == 'test1'


@pytest.mark.django_db
def test_Classes_API_read(admin_client):
  class_1 = Classes.objects.create(name="test1")
  assert Classes.objects.count() == 1
  class_id = class_1.id
  url = reverse('classes-detail', args=(class_id,))
  response = admin_client.get(url)
  assert response.status_code == 200
  assert Classes.objects.first().name == 'test1'


@pytest.mark.django_db
def test_Classes_API_update(admin_client):
  class_1 = Classes.objects.create(name="test1")
  assert Classes.objects.count() == 1
  class_id = class_1.id
  url = reverse('classes-detail', args=(class_id,))
  data = {'name': "test2"}
  json_data = json.dumps(data)
  response = admin_client.put(url, data=json_data, content_type="application/json")
  assert response.status_code == 200
  class_1.refresh_from_db()
  assert Classes.objects.first().name == 'test2'


@pytest.mark.django_db
def test_Classes_API_delete(admin_client):
  class_1 = Classes.objects.create(name="test1")
  assert Classes.objects.count() == 1
  class_id = class_1.id
  url = reverse('classes-detail', args=(class_id,))
  data = {'name': "test2"}
  json_data = json.dumps(data)
  response = admin_client.delete(url, data=json_data, content_type="application/json")
  assert response.status_code == 204
  assert Classes.objects.count() == 0

# @pytest.mark.django_db
# def test_not_owner_view(auto_login_user):
#    client, user = auto_login_user()
#    client.login(username=user.username, password="some_passwors")
#    Topic.objects.create(owner=user)
   
#    client, another_user = auto_login_user()
#    client.login(username=another_user.username, password="some_passwors")
#    topic = Topic.objects.all().first()
   
#    url = reverse('apts:topic', args=[topic.id])
#    response = client.get(url)
#    assert response.status_code == 404


# @pytest.mark.django_db
# def test_view_topic_as_admin(admin_client, auto_login_user):
#    client, user = auto_login_user()
#    Topic.objects.create(owner=user)
#    client.logout()
   
#    topic = Topic.objects.all().first()
#    url = reverse('apts:topic', args=[topic.id])
   
#    response = client.get(url)
#    assert response.status_code == 302

#    client = admin_client
#    response = client.get(url)
#    assert response.status_code == 200


# @pytest.mark.django_db
# def test_view_topics_as_admin(admin_client):
#    url = reverse('apts:topics')
#    response = admin_client.get(url)
#    assert response.status_code == 200


# @pytest.mark.django_db
# def test_view_unauthorized(client):
#    url = reverse('apts:topics')
#    response = client.get(url)
#    assert response.status_code == 302



# pytest classbook\gen_test.py
  
# pytest classbook\gen_test.py --cov-report html --cov=app_test
# pytest classbook\gen_test.py --cov=app_test

