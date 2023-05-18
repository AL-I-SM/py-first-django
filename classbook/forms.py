from django import forms
from classbook.models import Classes, Disciplines, Teachers


# class ScoresForms(forms.Form):
#     score = forms.CharField(label='', required=False)
#     # score = forms.T(label='', required=False)


class SelectJournalForms(forms.Form):
    CURRENT_CLASS_CHOICES = [(_.id, _.name) for _ in Classes.objects.all()]
    DISCIPLINES_CHOICES = [(_.id, _.name) for _ in Disciplines.objects.all()]
    TEACHER_CLASS_CHOICES = [(_.id, _.first_name + " " + _.middle_name + " " + _.last_name) for _ in Teachers.objects.all()]
    current_class = forms.ChoiceField(label='Класс', choices=CURRENT_CLASS_CHOICES)
    discipline = forms.ChoiceField(label='Предмет', choices=DISCIPLINES_CHOICES)
    teacher = forms.ChoiceField(label='Преподаватель', choices=TEACHER_CLASS_CHOICES)
