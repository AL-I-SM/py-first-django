from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('journal', views.journal, name="journal"),
    # re_path(r'^books/$', views.BookListView.as_view(), name='books'),
]
