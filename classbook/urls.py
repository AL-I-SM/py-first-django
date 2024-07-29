from django.urls import path, re_path
from . import views
from .views import JournalView, ScheduleClassView, ScheduleTeacherView
from rest_framework.routers import SimpleRouter
from classbook.views import PupilsViewSet, LessonsViewSet, ClassesViewSet

router = SimpleRouter()
router.register('pupils/api', PupilsViewSet)
router.register('lessons/api', LessonsViewSet)
router.register('classes/api', ClassesViewSet)

urlpatterns = [
    path('', views.index, name="index"),
    path('pupils/', views.pupils, name='pupils'),
    path('pupils_vue/', views.pupils_vue, name='pupils_vue'),
    path('pupil/<int:pupil>/', views.pupil_edit, name='pupil_edit'),
    re_path(r'^pupil/update/(?P<pk>\d+)$', views.PupilUpdate.as_view(), name='pupil_update'),
    path('groups/', views.groups, name='groups'),
    path('group/<int:group>/', views.group_edit, name='group_edit'),
    path('journal/', views.journal_select, name="journal-select"),
    path('schedule_class/<int:group>/', ScheduleClassView.as_view(), name="schedule_class"),
    path('schedule_techer/<int:teacher>/', ScheduleTeacherView.as_view(), name="schedule_teacher"),
    path('journal/<int:group>/<int:discipline>/<int:teacher>/', JournalView.as_view(), name="journal"),
    
    # re_path('score', views.score, name="score"),
]

urlpatterns += router.urls