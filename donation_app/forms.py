from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.forms import forms, EmailField, PasswordInput, CharField, TextInput, EmailInput

from donation_app.models import MyUser


class UserCreateForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', )
        widgets = {
            'email': EmailInput(attrs={'placeholder': 'Email'}),
            'first_name': TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': TextInput(attrs={'placeholder': 'Nazwisko'}),
        }

    password1 = CharField(
        label=("Password"),
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Hasło'}),
    )
    password2 = CharField(
        label=("Password confirmation"),
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Powtórz hasło'}),
        strip=False,
    )
