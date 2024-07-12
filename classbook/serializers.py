
from rest_framework.serializers import ModelSerializer

from classbook.models import Pupils, Classes, Disciplines, Lessons

class PupilsSerializer(ModelSerializer):
    class Meta:
        model = Pupils
        fields = ['id', 'group', 'sub_group']

class GroupsSerializer(ModelSerializer):
    class Meta:
        model = Classes
        fields = ['id', 'name']

class DisciplinesSerializer(ModelSerializer):
    class Meta:
        model = Disciplines
        fields = ['id', 'name']

class LessonsSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['id', 'date', 'group', 'teacher', 'topic']

