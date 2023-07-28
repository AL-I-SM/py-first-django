from django import forms
from django.forms import ModelForm
from django.urls import reverse_lazy

from classbook.models import Classes, Disciplines, Teachers, Pupils


class PupilEditForm(ModelForm):
    class Meta:
        model = Pupils
        # exclude = []
        fields = ['first_name', 'last_name', 'middle_name', 'sex',
                  'date_of_birth', 'sub_group', 'group']


class PupilsForm(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=200)
    last_name = forms.CharField(label="Фамилия", max_length=200)
    middle_name = forms.CharField(label="Отчество", max_length=200)
    date_of_birth = forms.CharField(label="Дата рождения", max_length=200)
    sex = forms.CharField(label="Пол", max_length=200)


class GroupsForm(forms.Form):
    name = forms.CharField(label='Название класса', max_length=200)
    teacher = forms.ChoiceField(label='Классный руководитель',
                                choices=[(_.id, _.first_name + " " + _.middle_name + " " + _.last_name)
                                         for _ in Teachers.objects.all()])


class SelectGroupScheduleForms(forms.Form):
    GROUP = [(_.id, _.name) for _ in Classes.objects.all()]
    group = forms.ChoiceField(label='Класс', choices=GROUP)


class SelectTeacherScheduleForms(forms.Form):
    TEACHERS = [(_.id, _.last_name) for _ in Teachers.objects.all()]
    teacher = forms.ChoiceField(label='Пероподаватель', choices=TEACHERS)


class SelectJournalForms(forms.Form):
    GROUP = [(_.id, _.name) for _ in Classes.objects.all()]
    DISCIPLINES_CHOICES = [(_.id, _.name) for _ in Disciplines.objects.all()]
    TEACHER_CLASS_CHOICES = [(_.id, _.first_name + " " + _.middle_name + " " + _.last_name) for _ in
                             Teachers.objects.all()]

    group = forms.ChoiceField(label='Класс', choices=GROUP)
    discipline = forms.ChoiceField(label='Предмет', choices=DISCIPLINES_CHOICES)
    teacher = forms.ChoiceField(label='Преподаватель', choices=TEACHER_CLASS_CHOICES)
