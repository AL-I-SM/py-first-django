from django.urls import re_path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(template_name='users/login.html'), name="login"),
    re_path(r'^logout/$', LogoutView.as_view(next_page='users:login'), name="logout"),
    re_path(r'^register/$', views.register, name="register"),
]