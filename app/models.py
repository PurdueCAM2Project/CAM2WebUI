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
