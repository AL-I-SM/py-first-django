from django.urls import path, re_path, include
from . import views

from django.contrib import admin


urlpatterns = [
    path('', views.index, name='index'),
]