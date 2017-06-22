from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.validators import validateURL, validateEmail,validateMonth, validateYear, validateName #


class RegisterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(verbose_name='Department(Optional)', max_length=100, blank=True, null=True)
    organization = models.CharField(verbose_name='Organization(Optional)', max_length=100, blank=True, null=True)
    title = models.CharField(verbose_name='Title(Optional)', max_length=100, blank=True, null=True)
    country = models.CharField(verbose_name='Country(Optional)', max_length=50, blank=True, null=True)
    about= models.TextField(verbose_name='About(Optional)', max_length=500, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)


class FAQ(models.Model):
    question = models.CharField(verbose_name='FAQ question', max_length=200)
    answer = models.CharField(verbose_name='FAQ answer', max_length=500)
    def __str__(self):
        return "{0}".format(self.question)


class History(models.Model):
    month = models.PositiveIntegerField(validators=[validateMonth])
    year = models.PositiveIntegerField(validators=[validateYear])
    event = models.CharField(verbose_name='History Details', max_length=500)
    def __str__(self):
        event = self.event[:50] if len(self.event) > 50 else self.event
        return "{0}/{1} {2}...".format(self.month, self.year, event)


class Publication(models.Model):
    paperinfo = models.CharField(verbose_name='Publication Details', max_length=500)
    paperlink = models.CharField(verbose_name='Publication Paper Link (Optional)', max_length=300, blank=True, null=True, validators=[validateURL])
    def __str__(self):
        paperinfo = self.paperinfo[:100] if len(self.paperinfo) > 100 else self.paperinfo
        return "{0}...".format(paperinfo)


class Team(models.Model):
    teamimg = models.CharField(verbose_name='Team Image', max_length=300, validators=[validateURL])


class Leader(models.Model):
    leaderimg = models.CharField(verbose_name='Leader Image', max_length=300, validators=[validateURL])
    leadertitle = models.CharField(verbose_name='Leader Title', max_length=50, validators=[validateName])
    leadername = models.CharField(verbose_name='Leader Name', max_length=50, validators=[validateName])
    leaderpagelink = models.CharField(verbose_name='Leader Page Link (Optional)', max_length=300, blank=True, null=True, validators=[validateURL])
    def __str__(self):
        return "{0}".format(self.leadername)


class Member(models.Model):
    membername = models.CharField(verbose_name='Member Name', max_length=50, validators=[validateName])
    memberimg = models.CharField(verbose_name='Member Image', max_length=300, blank=True, null=True, validators=[validateURL])
    iscurrentmember = models.BooleanField(verbose_name='Is Current Member')
    def __str__(self):
        return "{0}".format(self.membername)

