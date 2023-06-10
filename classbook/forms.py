from django import forms
from classbook.models import Classes, Disciplines, Teachers


class SelectScheduleForms(forms.Form):
    GROUP = [(_.id, _.name) for _ in Classes.objects.all()]
    group = forms.ChoiceField(label='Класс', choices=GROUP)


class SelectJournalForms(forms.Form):
    GROUP = [(_.id, _.name) for _ in Classes.objects.all()]
    DISCIPLINES_CHOICES = [(_.id, _.name) for _ in Disciplines.objects.all()]
    TEACHER_CLASS_CHOICES = [(_.id, _.first_name + " " + _.middle_name + " " + _.last_name) for _ in Teachers.objects.all()]

    group = forms.ChoiceField(label='Класс', choices=GROUP)
    discipline = forms.ChoiceField(label='Предмет', choices=DISCIPLINES_CHOICES)
    teacher = forms.ChoiceField(label='Преподаватель', choices=TEACHER_CLASS_CHOICES)
