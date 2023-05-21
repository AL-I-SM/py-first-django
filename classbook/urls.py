from django.urls import path, re_path
from . import views
from .views import JournalView, ScheduleView


urlpatterns = [
    path('', views.index, name="index"),
    path('journal/', views.journal_select, name="journal-select"),
    path('schedule/', ScheduleView.as_view(), name="schedule"),
    path('journal/<int:current_class>/<int:discipline>/<int:teacher>/', JournalView.as_view(), name="journal"),
    re_path('score', views.score, name="score"),
]
