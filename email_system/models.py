from django.contrib.auth.models import User
from django.db import models

class MailMessage(models.Model):
    email_all_users = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, blank=True, null=True)
    subject = models.CharField(max_length=255, )
    message = models.TextField(blank=True, null=True)


    #attachment = models.FileField(blank=True, null=True)

    #def remove_file(self):
    #    models.FieldFile.delete()



    class Meta:
        verbose_name = "Send Email to User"
        verbose_name_plural = "Emails to send"
