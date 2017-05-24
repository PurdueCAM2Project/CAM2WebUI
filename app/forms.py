from django import forms
from django.contrib.auth.forms import UserCreationForm #username, password
from django.contrib.auth.models import User
from .models import RegisterUser

class RegistrationForm(UserCreationForm):
    #To add more imformation, simply define below and add it to fields
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    """
    organization = forms.CharField(label='Organization (Optional)', max_length=150, required=False)
    title = forms.CharField(label='Title (Optional)', max_length=150, required=False)
    country = forms.CharField(label='Country (Optional)', max_length=150, required=False)
    please_tell_us= forms.CharField(widget=forms.Textarea, label='Please tell us how you heard about the CAM² System. (Optional)',
                                     max_length=500, required=False)
    """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class AdditionalForm(forms.ModelForm):
    class Meta:
        model = RegisterUser
        fields = ('department', 'organization', 'title', 'country', 'about')

class LoginForm(forms.Form):
	username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class' : 'loginput'}),required=True)
	password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class' : 'loginput'}), required=True)
