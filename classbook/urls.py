from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('journal/', views.journal_select, name="journal-select"),
    path('journal/<int:current_class>/<int:discipline>/<int:teacher>/', views.journal, name="journal"),
    re_path('score', views.score, name="score"),
]
