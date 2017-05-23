from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    organization = forms.CharField(max_length=150, required=False, help_text='Optional')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'organization', 'email', 'password1', 'password2',)

class LoginForm(forms.Form):
	username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class' : 'loginput'}),required=True)
	password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class' : 'loginput'}), required=True)
