from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords #need to do pip install django-simple-history


class Profile(models.Model):
    """Extends built-in User model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    occupation = models.CharField(max_length=30, blank=True)
    organization = models.CharField(max_length=60, blank=True)
    use_case = models.TextField(max_length=140, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates a Profile object whenever a User is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Updates the assocaited Profile object whenever a User is updated."""
    instance.profile.save()


#a model to represent a group of camera urls that a user has downloaded
class User_Camera_Selection(models.Model):
    #define the name of each object in the model
    def __str__(self):
        return self.user_obj.user.username + "'s camera selection"

    def __unicode__(self):
        return self.user_obj.user.username + "'s camera selection"

    # associate to one User table
    user_obj = models.OneToOneField(User, blank=True, null=True)

    # selection info
    number_of_selection = models.IntegerField(default=0)
    date_of_download = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

#the details of each camera selected by the user
class Camera_Detail(models.Model):
    # define the name of each object in the model
    def __str__(self):
        return self.url

    def __unicode__(self):
        return self.url

    # associate to one User Camera Selection table
    user_selection_obj = models.ForeignKey(User_Camera_Selection, blank=True, null=True)

    # camera information
    name = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=200)
    id = models.CharField(max_length=200)
    date_of_selection = models.DateTimeField(auto_now_add=True)
    frequency_of_selection = models.IntegerField(default=0)
    history = HistoricalRecords()