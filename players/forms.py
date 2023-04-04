from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta (UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


class UserForm(forms.Form):
    name = forms.CharField(label="Имя", widget=forms.Textarea)
    age = forms.IntegerField(label="Возраст")
    boolean = forms.BooleanField()
    file = forms.FileField()
    data = forms.DateField()
    vyb = forms.NullBooleanField(label="Yes?")
