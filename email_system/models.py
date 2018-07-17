from django.contrib.auth.models import User
from django.db import models


class ContactModel(models.Model):
    name=models.CharField(verbose_name='Name', max_length=100, blank=True, null=True)
    from_email=models.EmailField()
    subject=models.CharField(verbose_name='Subject', max_length=100, blank=True, null=True)
    message=models.CharField(verbose_name='Message', max_length=500, blank=True, null=True)
    date=models.DateField(blank=True, null=True)
    def __str__(self):
        return "{0}".format(self.subject)

class JoinModel(models.Model):
    name=models.CharField(verbose_name='Name', max_length=100, blank=True, null=True)
    from_email=models.EmailField()
    major=models.CharField(verbose_name='Major', max_length=1000, blank=True, null=True)
    gradDate=models.CharField(verbose_name='Graduation Date', max_length=1000, blank=True, null=True)
    courses=models.CharField(verbose_name='Courses Taken', max_length=1000, blank=True, null=True)
    languages=models.CharField(verbose_name='Programming Languages', max_length=1000, blank=True, null=True)
    tools=models.CharField(verbose_name='Development Tools', max_length=1000, blank=True, null=True)
    whyCAM2=models.CharField(verbose_name='Reason to Join', max_length=1000, blank=True, null=True)
    anythingElse=models.CharField(verbose_name='Additional Information', max_length=1000, blank=True, null=True)
    date=models.DateField(blank=True, null=True)
    def __str__(self):
        return "{0}".format(self.name)

