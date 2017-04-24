from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django import forms
from collections import OrderedDict
import re


class UserCreateForm(UserCreationForm):

    """Initialize the form."""
    username = forms.CharField(label = 'Username', max_length = 30)
    email = forms.EmailField(label = 'Email')
    password1 = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)
    location = forms.CharField(label = 'Location', max_length = 100)
    occuption = forms.CharField(label = 'Occuption', max_length = 100)
    organization = forms.CharField(label = 'Organization', max_length = 100)

    class Meta:
	model = User
	fields = ("username","email","password1","password2","location","occuption","organization")


    """Save the user infor"""
    def save(self,commit=True):
	    user = super(UserCreationForm,self).save(commit=False)
	    user.set_password(self.cleaned_data["password1"])
	    if commit:
	        user.save()
	    return user

    
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


class ContactForm(forms.Form):
     contact_name = forms.CharField(required=True,max_length = 30)
     contact_email=forms.EmailField(required=True,max_length = 100)
     subject = forms.CharField(required=True,max_length = 100)
     message = forms.CharField(required=True,widget=forms.Textarea)


# class PasswordChangeForm(SetPasswordForm):
#     """forms that allow user to change password by enter the old password"""
#     error_message = dict(SetPasswordForm.error_messages, **{
#         'password_incorrect': _("wrong password input."),
#     })
#     old_password = forms.CharField(label=_("Old password"),
#                                    widget=forms.PasswordInput)
#
#     def clean_old_password(self):
#         """Validates that the old_password field is correct."""
#         old_password = self.cleaned_data["old_password"]
#         if not self.user.check_password(old_password):
#             raise forms.ValidationError(
#                 self.error_messages['password_incorrect'],
#                 code='password_incorrect',
#             )
#         return old_password

	




