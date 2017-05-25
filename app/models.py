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
