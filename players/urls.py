from django.urls import re_path, include, path, reverse_lazy
from players.views import dashboard, register2
# from django.contrib.auth import views
from players import views

reverse_lazy('password_reset_confirm', 'players:password_reset_confirm')

urlpatterns = [
    path('players', views.index),
    path('create', views.create),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^dashboard/$', dashboard, name='dashboard'),
    re_path(r'^register2/$', register2, name="register2"),
]

