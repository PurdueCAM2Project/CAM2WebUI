from django.db import models

# Create your models here.


# User Table is used to store the information of user's personal information and github account information
class User(models.Model):
  #user information
  full_name = models.CharField(max_length=100, help_text="Full Name")
  user_name = models.CharField(max_length=100, help_text="User Name")
  user_email = models.CharField(max_length=200, help_text="Email")
  account_number = models.CharField(max_length=200)
  account_password = models.CharField(max_length=200)
  current_occupation_choices = (
    'Student','Teacher','Professor','Programmer','etc'
  ) #this field can be changed to next field
  current_occupation = models.CharField(max_length=50, blank=True, help_text="Current Occupation")
  user_company = models.CharField(max_length=50, blank=True, help_text="Company You Work For")
  user_location = models.CharField(max_length=50, blank=True, help_text="Where You Leave")
  reason_of_use = models.CharField(max_length=300, blank=True, help_text="How do you find this website?")
  registration_time = models.DateTimeField(auto_now_add=True)
  #user api
  api_key = models.CharField(max_length=200)
  #user information associated with github, user name is unique to each user
  github_name = models.CharField(max_length=200)
  github_email = models.CharField(max_length=200)
  github_bio = models.CharField(max_length=200)
  company_from_github = models.CharField(max_length=200)
  location_from_github = models.CharField(max_length=200)

