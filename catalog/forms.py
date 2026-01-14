from django import forms
from datetime import date
from django.forms import ModelForm
from .models import Book, Author


class AuthorsForms(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}),
        }

class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']
