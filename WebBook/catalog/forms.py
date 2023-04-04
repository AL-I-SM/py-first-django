from django import forms
from datetime import date
from django.forms import ModelForm
from .models import Book


class AuthorsForms(forms.Form):
    first_name = forms.CharField(label="Имя автора")
    last_name = forms.CharField(label="Фамилия автора")
    date_of_birth = forms.DateField(label="", initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={type: 'date'}))
    date_of_death = forms.DateField(label="", initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={type: 'date'}))


class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']
