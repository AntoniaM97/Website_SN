from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "email",

        ]


class LogInForm(forms.Form):
    user_name = forms.CharField(max_length=60)
    user_password = forms.CharField(max_length=60, widget=forms.PasswordInput)

