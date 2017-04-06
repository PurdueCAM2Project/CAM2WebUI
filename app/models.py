from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class CameraSelection(models.Model):
    """represents a group of camera URLs"""

    def __str__(self):
        return self.name

    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30)  # TODO: Add default that looks at date
    active = models.BooleanField(default=True)

class CameraDetail(models.Model):
    """the details of each camera selected by the user"""

    def __str__(self):
        return self.name

    selection = models.ForeignKey(CameraSelection)
    name = models.CharField(max_length=30)  # TODO: come up with default case
    url = models.CharField(max_length=200)
    cam_id = models.CharField(max_length=200)

class SelectionDownload(models.Model):
    """represents a single download of a selection"""

    def __str__(self):
        return self.selection  # TODO: Also return date and/or user

    selection = models.ForeignKey(CameraSelection)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
