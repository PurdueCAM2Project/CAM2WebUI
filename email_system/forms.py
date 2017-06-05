from django import forms
from email_system.models import MailMessage


class MailForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        if MailMessage.email_all_users:
            fields = ('email', 'email_all_users', 'subject', 'message')
        else :
            fields = ('email', 'subject', 'message')