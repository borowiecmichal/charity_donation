from django.contrib.auth import password_validation, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import EmailField, PasswordInput, CharField, TextInput, EmailInput, ModelForm, \
    CheckboxSelectMultiple
from django import forms
from django.utils.text import capfirst

from donation_app.models import MyUser, Donation


class UserCreateForm(UserCreationForm):
    password1 = CharField(
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Hasło'}),
    )
    password2 = CharField(
        widget=PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Powtórz hasło'}),
        strip=False,
    )

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email',)
        widgets = {
            'email': EmailInput(attrs={'placeholder': 'Email'}),
            'first_name': TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': TextInput(attrs={'placeholder': 'Nazwisko'}),
        }


UserModel = get_user_model()


class LoginForm(AuthenticationForm):
    email = EmailField(widget=EmailInput(attrs={'autofocus': True, 'placeholder': 'Email'}))
    password = CharField(
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder': 'Hasło'}),
    )
    field_order = ['email', 'password']

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UpdateUserForm(ModelForm):
    field_order = ['email', 'first_name', 'last_name']

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email',)
        widgets = {
            'email': EmailInput(attrs={'placeholder': 'Email'}),
            'first_name': TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': TextInput(attrs={'placeholder': 'Nazwisko'}),
        }


class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = (
            'categories', 'quantity', 'institution', 'address', 'city', 'zip_code', 'phone_number', 'pick_up_date',
            'pick_up_time', 'pick_up_comment')

        widgets = {
            'categories': CheckboxSelectMultiple,
            'institution': forms.RadioSelect
        }

        # widgets = {
        #     'email': EmailInput(attrs={'placeholder': 'Email'}),
        #     'first_name': TextInput(attrs={'placeholder': 'Imię'}),
        #     'last_name': TextInput(attrs={'placeholder': 'Nazwisko'}),
        # }
