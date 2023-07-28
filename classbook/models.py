from django.contrib.auth.models import AbstractUser
from django.db import models

SCORE_CHOICES = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, 'н'))
SIMPLE_SCORE_CHOICES = ('0', '1', '2', '3', '4', '5', 'н')


class User(AbstractUser):
    middle_name = models.CharField('Отчество', max_length=50)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    sex = models.CharField('Пол', choices=(('М', 'М'), ('Ж', 'Ж')), max_length=1)


class Classes(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class Positions(models.Model):
    position = models.CharField("Звание", max_length=50)

    class Meta:
        verbose_name = "Звания"

    def __str__(self):
        return self.position


class Pupils(User):
    group = models.ForeignKey('Classes', on_delete=models.PROTECT, verbose_name="Класс")
    sub_group = models.SmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Ученик'

    def __str__(self):
        return self.last_name + " " + self.first_name


class Teachers(User):
    has_class = models.ManyToManyField('Classes', verbose_name="Классный руководитель:")
    can_teach = models.ManyToManyField('Disciplines', verbose_name="Может преподавать:")
    position = models.ForeignKey('Positions', on_delete=models.PROTECT, verbose_name="Звание")

    class Meta:
        verbose_name = 'Преподаватель'

    def __str__(self):
        return self.last_name + " " + self.first_name + " " + self.middle_name


class Disciplines(models.Model):
    name = models.CharField("Предметы", max_length=50)

    class Meta:
        verbose_name = "Предмет"

    def __str__(self):
        return self.name


class KTP(models.Model):
    discipline = models.ForeignKey('Disciplines', on_delete=models.PROTECT, verbose_name="КТП")
    lesson_number = models.SmallIntegerField()
    home_work = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    section = models.CharField(max_length=255)

    def __str__(self):
        return str(self.lesson_number)


class Lessons(models.Model):
    discipline = models.ForeignKey('Disciplines', on_delete=models.PROTECT)
    date = models.DateField(blank=True, null=True)
    topic = models.CharField(max_length=255)
    home_work = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    group = models.ForeignKey('Classes', on_delete=models.PROTECT, verbose_name="Класс")
    teacher = models.ForeignKey('Teachers', on_delete=models.DO_NOTHING)
    number = models.SmallIntegerField(blank=True)


class Days(models.Model):
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return str(self.date)


class Schedule(models.Model):
    week = models.SmallIntegerField()
    discipline = models.ForeignKey('Disciplines', on_delete=models.PROTECT, null=True)
    day = models.SmallIntegerField(blank=True, null=True)
    teacher = models.ForeignKey('Teachers', related_name='prime_teacher', on_delete=models.PROTECT)
    alt_teacher = models.ForeignKey('Teachers', related_name='alt_teacher', null=True, blank=True, on_delete=models.PROTECT)
    group = models.ForeignKey('Classes', on_delete=models.PROTECT, verbose_name="Класс")
    cabinet = models.CharField(max_length=25, null=True)
    extra_info = models.CharField(max_length=255, null=True)
    number = models.ForeignKey('TimeLessons', on_delete=models.PROTECT)
    sub_group = models.SmallIntegerField(default=1)


class TimeLessons(models.Model):
    number = models.SmallIntegerField()
    variant = models.SmallIntegerField()
    lesson_time = models.TimeField()
    rest_length = models.TimeField()


class Score(models.Model):
    date = models.DateField(auto_created=True)
    score = models.CharField(max_length=25, choices=SCORE_CHOICES, verbose_name='Оценка')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    pupil = models.ForeignKey('Pupils', on_delete=models.PROTECT, null=True)
    teacher = models.ForeignKey('Teachers', on_delete=models.PROTECT, null=True)
    discipline = models.ForeignKey('Disciplines', on_delete=models.PROTECT, null=True)
    extra = models.CharField(max_length=250, null=True)
    lesson = models.ForeignKey('Lessons', on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=0)
