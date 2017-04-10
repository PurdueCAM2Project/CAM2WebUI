from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django import forms
import re


class RegistrationForm(forms.ModelForm):

    """Initialize the form."""
    username = forms.CharField(label = 'Username', max_length = 30)
    email = forms.EmailField(label = 'Email')
    password1 = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)
    location = forms.CharField(label = 'Location', max_length = 100)
    occuption = forms.CharField(label = 'Occuption', max_length = 100)
    organization = forms.CharField(label = 'Organization', max_length = 100)

    """Check to see the user enterd the right password"""
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            else:
		raise forms.ValidationError('Passwords entered do not match.')

    """Check if the Username is valid"""
    def clean_username(self):
        username = self.cleaned_data['username']
	if not re.search(r'^\w+$',username):
	    raise forms.ValidationError('invlid username')
	try:
	    User.object.get(username = Username)
	except ObjectDoesNotExist:
	    return Username
	raise forms.ValidationError('Username is already taken.')










