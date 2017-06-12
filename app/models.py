from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class RegisterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(verbose_name='Department(Optional)', max_length=100, blank=True, null=True)
    organization = models.CharField(verbose_name='Organization(Optional)', max_length=100, blank=True, null=True)
    title = models.CharField(verbose_name='Title(Optional)', max_length=100, blank=True, null=True)
    country = models.CharField(verbose_name='Country(Optional)', max_length=50, blank=True, null=True)
    about= models.TextField(verbose_name='About(Optional)', max_length=500, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=500)

class History(models.Model):
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    event = models.CharField(max_length=500)

class Publication(models.Model):
    paperinfo = models.CharField(max_length=500)
    paperlink = models.CharField(max_length=300, blank=True, null=True)

class Team(models.Model):
    teamimg = models.CharField(max_length=300)

class Leader(models.Model):
    leaderimg = models.CharField(max_length=300)
    leadertitle = models.CharField(max_length=50)
    leadername = models.CharField(max_length=50)
    leaderpagelink = models.CharField(max_length=300)

class CurrentMember(models.Model):
    currentmemberimg = models.CharField(max_length=300)
    currentmembername = models.CharField(max_length=50)

class OldMember(models.Model):
    oldmembername = models.CharField(max_length=50)
