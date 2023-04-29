from django.contrib.auth.models import AbstractUser
from django.db import models

SCORE_CHOICES = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))


class User(AbstractUser):
    middle_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField('Пол', choices=((0, 'М'), (1, 'Ж')), max_length=1)


class Classes(models.Model):
    name = models.CharField(max_length=5)


class Pupils(User):
    curren_class = models.ForeignKey('Classes', on_delete=models.PROTECT)


class Positions(models.Model):
    position = models.CharField(max_length=50)


class Teachers(User):
    has_class = models.ManyToManyField('Classes')
    can_teach = models.ManyToManyField('Disciplines')
    position = models.ForeignKey('Positions', on_delete=models.PROTECT)


class Disciplines(models.Model):
    name = models.CharField(max_length=50)


class KTP(models.Model):
    discipline = models.ForeignKey('Disciplines', on_delete=models.PROTECT)
    lesson_number = models.SmallIntegerField()
    home_work = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    section = models.CharField(max_length=255)


class Lessons(models.Model):
    discipline = models.ManyToManyField('Disciplines')
    teacher = models.ManyToManyField('Teachers', related_name='prime_teacher')
    date = models.DateField(blank=True, null=True)
    alt_teacher = models.ManyToManyField('Teachers', related_name='alt_teacher')
    topic = models.CharField(max_length=255)
    home_work = models.CharField(max_length=255)


class Holidays(models.Model):
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=255)


class Schedule(models.Model):
    date = models.DateField(blank=True, null=True)
    week = models.SmallIntegerField()
    teacher = models.ForeignKey('Teachers', on_delete=models.PROTECT, null=True)
    cabinet = models.CharField(max_length=25)
    discipline = models.ForeignKey('Disciplines', on_delete=models.PROTECT, null=True)
    extra_info = models.CharField(max_length=255)


class Score(models.Model):
    date = models.DateField(auto_created=True)
    score = models.SmallIntegerField(choices=SCORE_CHOICES, verbose_name='Оценка')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    pupil = models.ForeignKey('Pupils', on_delete=models.PROTECT, null=True)
    teacher = models.ForeignKey('Teachers', on_delete=models.PROTECT, null=True)
    discipline = models.ForeignKey('Disciplines', on_delete=models.PROTECT, null=True)
