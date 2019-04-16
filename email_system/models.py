import app.models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

class ContactModel(models.Model):
    class Meta:
        verbose_name = 'contact'
    name=models.CharField(verbose_name='Name', max_length=100, blank=True, null=True)
    from_email=models.EmailField()
    subject=models.CharField(verbose_name='Subject', max_length=100, blank=True, null=True)
    message=models.CharField(verbose_name='Message', max_length=500, blank=True, null=True)
    date=models.DateField(blank=True, null=True)
    def __str__(self):
        return "{0}".format(self.subject)

class JoinModel(models.Model):
    class Meta:
        verbose_name = 'application'
    name=models.CharField(verbose_name='Name', max_length=100)
    from_email=models.EmailField()
    major=models.CharField(verbose_name='Major', max_length=1000)
    gradDate=models.CharField(verbose_name='Graduation Date', max_length=1000)
    courses=models.CharField(verbose_name='Courses Taken', max_length=1000, blank=True, null=True)
    languages=models.CharField(verbose_name='Programming Languages', max_length=1000)
    tools=models.CharField(verbose_name='Development Tools', max_length=1000, blank=True, null=True)
    whyCAM2=models.CharField(verbose_name='Reason to Join', max_length=1000)
    anythingElse=models.CharField(verbose_name='Additional Information', max_length=1000, blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    favoriteTeams=models.CharField(verbose_name='4 Favorite Teams', max_length=150, blank=True, null=True)
    knowledge=models.CharField(verbose_name='Knowledge in Various Fields', max_length=1000, blank=True, null=True)
    teamwork=models.CharField(verbose_name='Expirience in Teamwork', max_length=1000, blank=True, null=True)
    problem=models.CharField(verbose_name='Explain Problem', max_length=1000, blank=True, null=True)
    futureLeader=models.BooleanField(verbose_name='Wants to be a Leader', blank=True)
    semester=models.ForeignKey('ApplicationDeadline', verbose_name='Application Semester', on_delete=models.CASCADE)
    def __str__(self):
        return "{0}".format(self.name)

class ApplicationDeadline(models.Model):
    name=models.CharField(verbose_name='Application Period', max_length=6)
    show=models.BooleanField(verbose_name='Show the Deadline to the User?')
    date=models.DateTimeField(verbose_name='Cutoff Date')
    def __str__(self):
        return "{0} - {1}{2}".format(self.date, self.name, '' if self.show else ' (hidden)')
    def display_time():
        eastern = timezone('US/Eastern')
        return '{}'.format(date.astimezone(eastern).isoformat())
