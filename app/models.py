from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.validators import validateURL, validateEmail,validateMonth, validateYear, validateName 


class RegisterUser(models.Model):
    """Django model for user registration
    
    Contains information that structures the database for users, in particular the
    optional Additional Information that a user can give alongside their name, email,
    and other required fields.

    Attributes:
        user: A OneToOneField for the user's full name, connected to the model django.contrib.auth.models.User
        department: A CharField for the user's Department
        organization: A CharField for the user's Organization
        title: A CharField for the user's Job Title
        country: A CharField for the user's Country
        about: A CharField for any extra information the user wanted to share about themselves
        email_confirmed: A BooleanField that indicates whether or not a user has confirmed their
            email address using an activation link

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(verbose_name='Department(Optional)', max_length=100, blank=True, null=True)
    organization = models.CharField(verbose_name='Organization(Optional)', max_length=100, blank=True, null=True)
    title = models.CharField(verbose_name='Title(Optional)', max_length=100, blank=True, null=True)
    country = models.CharField(verbose_name='Country(Optional)', max_length=50, blank=True, null=True)
    about= models.TextField(verbose_name='About(Optional)', max_length=500, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)

class CAM2dbApi(models.Model):
    """Django model for apps that use the CAM2 Database API
    
    Contains information that structures the database for user-made apps that access the CAM2 API.

    Attributes:
        appname: A CharField for the name of the app
        user: A ForeignKey connected to the model django.contrib.auth.models.User for a specific user

    """
    appname = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,)


class FAQ(models.Model):
    """Django model for Frequently Asked Questions (FAQs)
    
    Contains information that structures the database for FAQs.

    Attributes:
        question: A CharField for the question frequently asked. Used to identify an instance of the model in the Admin software.
        answer: A CharField for the answer to that question

    """
    question = models.CharField(verbose_name='FAQ question', max_length=200)
    answer = models.CharField(verbose_name='FAQ answer', max_length=500)
    def __str__(self):
        return "{0}".format(self.question)


class History(models.Model):
    """Django model for CAM2's history
    
    Contains information that structures the database for the history of CAM2

    Attributes:
        month: A PositiveIntegerField for the month the event occured in
        year: A PositiveIntegerField for the year the event occured in
        event: A CharField for a description of the event

    """
    month = models.PositiveIntegerField(validators=[validateMonth])
    year = models.PositiveIntegerField(validators=[validateYear])
    event = models.CharField(verbose_name='History Details', max_length=500)
    def __str__(self):
        event = self.event[:50] if len(self.event) > 50 else self.event
        return "{0}/{1} {2}...".format(self.month, self.year, event)


class Publication(models.Model):
    """Django model for publications
    
    Contains information that structures the database for CAM2's publications

    Attributes:
        paperinfo: A CharField for a description of the paper and its details
        paperlink: A CharField for a link to the paper, validated as a URL

    """
    paperinfo = models.CharField(verbose_name='Publication Details', max_length=500)
    paperlink = models.CharField(verbose_name='Publication Paper Link (Optional)', max_length=300, blank=True, null=True, validators=[validateURL])
    def __str__(self):
        paperinfo = self.paperinfo[:100] if len(self.paperinfo) > 100 else self.paperinfo
        return "{0}...".format(paperinfo)


class Team(models.Model):
    """Django model for an image of the CAM2Team
    
    Contains information that structures the database for the team photo

    Attributes:
        teamimg: A CharField for a link to an image, validated as an URL

    """
    teamimg = models.CharField(verbose_name='Team Image', max_length=300, validators=[validateURL])


class Leader(models.Model):
    """Django model for the team leaders' information
    
    Contains information that structures the database for the team leaders and advisors

    Attributes:
        leaderimg: A CharField for a link to an image, validated as an URL
        leadertitle: A CharField for the leader's Job Title
        leadername: A CharField for the leader's full name
        leaderpagelink: A CharField for a link to the leader's website, validated as an URL

    """
    leaderimg = models.CharField(verbose_name='Leader Image', max_length=300, validators=[validateURL])
    leadertitle = models.CharField(verbose_name='Leader Title', max_length=50)
    leadername = models.CharField(verbose_name='Leader Name', max_length=50, validators=[validateName])
    leaderpagelink = models.CharField(verbose_name='Leader Page Link (Optional)', max_length=300, blank=True, null=True, validators=[validateURL])
    def __str__(self):
        return "{0}".format(self.leadername)


class Member(models.Model):
    """Django model for team members
    
    Contains information that structures the database for CAM2 team members, both active and inactive

    Attributes:
        membername: A CharField for the team member's full name.
        memberimg: A CharField for an image URL for the team member. Should be blank if iscurrentmember is False.
        iscurrentmember: A BooleanField that indicates whether or not this team member is a current member

    """
    membername = models.CharField(verbose_name='Member Name', max_length=50, validators=[validateName])
    memberimg = models.CharField(verbose_name='Member Image', max_length=300, blank=True, null=True, validators=[validateURL])
    iscurrentmember = models.BooleanField(verbose_name='Is Current Member')

    TEAM = (
        ('I', "Image Analysis"),
        ('UI', "Web UI"),
        ('D+API', "API team"),
        ('One B', "One Billion Images Team"),
        ('Intel', "Intel Target Tracking")
    )

    subteam = models.CharField(verbose_name='Subteam', blank=True, max_length=50, choices=TEAM, default='blank')
    def __str__(self):
        return "{0}".format(self.membername)

