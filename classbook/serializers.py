
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from classbook.models import Pupils, Classes, Disciplines, Lessons, Score
from django.db.models import Avg

class PupilsSerializer(ModelSerializer):
    # score_average = serializers.SerializerMethodField()
        
    class Meta:
        model = Pupils
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'group', 'sub_group']

    # def get_score_average(self, instance):
    #     return Score.objects.filter(pupil=instance).aggregate(Avg('score'))['score__avg']


class ClassesSerializer(ModelSerializer):
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

