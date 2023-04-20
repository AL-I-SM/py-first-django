from django.urls import re_path, include, path, reverse_lazy
from players.views import dashboard, register_user
# from django.contrib.auth import views
from players import views

reverse_lazy('password_reset_confirm', 'players:password_reset_confirm')

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    # path('login/', views.login_user, name='login'),
    re_path(r'^register/$', register_user, name="register"),
]

