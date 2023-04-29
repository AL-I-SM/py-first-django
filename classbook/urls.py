from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    # re_path(r'^books/$', views.BookListView.as_view(), name='books'),
]
