from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.validators import validateURL, validateEmail,validateMonth, validateYear, validateName 

class Homepage(models.Model):
    """Django model for the homepage 

    Attributes:
         slideheader: A CharField for the title of the slide.
         slidedescrb: A CharField for the content of description of the slide. 
         slidelink: A CharField for the link of the image used in the slide.
         slidenum: A IntegerField for the number of the current slide. 

    """
    slideheader = models.CharField(verbose_name='Slide Header', max_length=500, blank=True)
    
    slidedescrb = models.CharField(verbose_name='Slide Description', max_length=300, blank=True, null=True)

    slidedescrb1 = models.CharField(verbose_name='Slide Description', max_length=300, blank=True, null=True)
    
    slidenum = models.IntegerField(verbose_name='Slide Number', blank=False, null=True)
    
    slidelink = models.CharField(verbose_name='Image Link', max_length=100, blank=True, null=True)
    
    def __str__(self):
        return "{0}".format(self.slideheader)


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
    paperinfo = models.CharField(verbose_name='Publication Details', max_length=1500)
    conference = models.CharField(verbose_name='Publication Conference', max_length=1500)
    authors = models.CharField(verbose_name='Publication Authors', max_length=1500)
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

class Collab(models.Model):
    """Django model for the team collaborators' information

    Contains information that structures the database for the collaborators

    Attributes:
         collabname: A CharField for the name of the collaborating organization
         collabdescr: A CharField for a brief description of the collaborator
         collablink: A CharField for a link to the collaborator's website, validated as a URL
         collabimg: A CharField for a link to the collaborator's logo, validated as a URL

    """
    collabname = models.CharField(verbose_name='Collaborator', max_length=100)
    collabdescr = models.CharField(verbose_name='Description', max_length=500, blank=True, null=True)
    collablink = models.CharField(verbose_name='Link to Site', max_length=300, blank=True, null=True, validators=[validateURL])
    collabimg = models.CharField(verbose_name='Collaborator Logo', max_length=300, blank=True, null=True, validators=[validateURL])
    def __str__(self):
        return "{0}".format(self.collabname)
    
class Sponsor(models.Model):
    """Django model for the team sponsors' information

    Contains information that structures the database for the sponsors

    Attributes:
         sponname: A CharField for the name of the collaborating organization
         spondescr: A CharField for a brief description of the sponsor
         sponlink: A CharField for a link to the sponsor's website, validated as a URL
         logolink: An image of the logo of the sponsor

    """
    sponname = models.CharField(verbose_name='Sponsor', max_length=100, blank=True)
    spondescr = models.CharField(verbose_name='Description', max_length=500, blank=True, null=True)
    sponlink = models.CharField(verbose_name='Link to Site', max_length=300, blank=True, null=True, validators=[validateURL])
    logolink = models.CharField(verbose_name='Link to Logo', max_length=300, blank=True, null=True, validators=[validateURL])
    def __str__(self):
        return "{0}".format(self.sponname)
    
class Calendar(models.Model):
    """Django model for group claendar
    
    Content to be decided.
    
    """
    calendarinfo = models.CharField(verbose_name="Calendar Information", max_length=100)

class Location(models.Model):
    """Django model for the office locations relevant to CAM2

    Contains information that structures the database for the office locations of CAM2

    Attributes:
        officename: A CharField for a descriptive name for the office listed
        officeroom: A CharField for the room number of the office
        officebldg: A CharField for the building in which the office is located
        officeaddr: A CharField for the street address of the office building
        officecity: A CharField for the city of the office building
        officestate: A CharField for the abbreviation of the state of the office building
        officezip: A CharField for the Zip Code of the office building
        officenum: A CharField for the phone number of the office

    """
    officename = models.CharField(verbose_name='Office Name', max_length=100)
    officeroom = models.CharField(verbose_name='Room Number', max_length=50, blank=True, null=True)
    officebldg = models.CharField(verbose_name='Building', max_length=100, blank=True, null=True)
    officeaddr = models.CharField(verbose_name='Address', max_length=100)
    officecity = models.CharField(verbose_name='City', max_length=100)
    officestate = models.CharField(verbose_name='State', max_length=2)
    officezip = models.CharField(verbose_name='Zip Code', max_length=50)
    officenum = models.CharField(verbose_name='Phone Number', max_length=50, blank=True, null=True)
    def __str__(self):
        return "{0}".format(self.officename)


class Member(models.Model):
    """Django model for team members
    
    Contains information that structures the database for CAM2 team members, both active and inactive

    Attributes:
        membername: A CharField for the team member's full name.
        memberimg: A CharField for an image URL for the team member. Should be blank if iscurrentmember is False.
        iscurrentmember: A BooleanField that indicates whether or not this team member is a current member
        subteam: A CharField that indicates which subteam this member belongs to. Default is blank

    """
    membername = models.CharField(verbose_name='Member Name', max_length=50, validators=[validateName])
    memberimg = models.CharField(verbose_name='Member Image', max_length=300, blank=True, null=True, validators=[validateURL])
    iscurrentmember = models.BooleanField(verbose_name='Is Current Member')

    TEAM = (
        ('I', "Image Analysis"),
        ('UI', "Web UI"),
        ('D+API', "API team"),
        ('PP', "Parrellel Perforamce"),
        ('RM', "Reserouce Management"),
        ('SE', "Software Engineering"),
        ('MA', "Mobile App"),
        ('CR', "Camera Reliability"),
        ('CD', "Camera Discovery"),
        ('TL', "Transfer Learning"),
        ('AT', "Active Training"),
        ('ID', "Image Database"),
        ('DV', "Drone Video"),
        ('FIA', "Forest Inventory Analysis"),   
        ('HB', "Human Behavior"),
        ('CS', "Crowdsourcing"),
        ('Intel', "Embedded Computer Vision")
    )

    subteam = models.CharField(verbose_name='Subteam', blank=True, max_length=50, choices=TEAM, default='blank')
    def __str__(self):
        return "{0}".format(self.membername)

class Poster(models.Model):
    """Django model for Posters

    Contains information that structures database for posters for CAM2

    Attributes:
        posterimg: A CharField for an image URL for the poster.
    """

    posterimg = models.CharField(verbose_name='Poster Image', max_length=300, validators=[validateURL])

class ReportedCamera(models.Model):
    """Django model for cameras reported as having missing images

    Contains information that structures the database for missing cameras

    Attributes:
        cameraID: A CharField for the ID of the reported camera.
        reporttime: A DateField for the time at which the camera was reported.
    """
    cameraID = models.CharField(verbose_name='Camera ID', max_length=100)
    reporttime = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return "{0}".format(self.cameraID)

