from django import forms
from django.contrib.auth.forms import UserCreationForm #username, password
from django.contrib.auth.models import User
from .models import RegisterUser, CAM2dbApi

class RegistrationForm(UserCreationForm):
    """Django form for new user registration
    
    Contains information used to register new users, based on the Django standard model for Users

    Attributes:
        first_name: A CharField for the user's First Name
        last_name: A CharField for the user's Last Name
        email: An EmailField for the user's Email address

    """
    #To add more imformation, simply define below and add it to fields
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        """Includes additional fields based on fields found within django.contrib.auth.models.User
    
        Adds information needed to create a form for registrating a user using Django's admin system.

        Attributes:
            model: the Django Model the added information is based on
            fields: a tuple of fields drawn from model to be used in the form
        """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        """Validates an email input by checking it against the database of current users
    
        Checks the email addresses of current active users and determines if the given email is in use.

        Returns:
            a cleaned version of the given email address.

        Raises:
            forms.ValidationError: the given email is associated with another user already and cannot be used again
        """
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email has already been used")
        return data

class AdditionalForm(forms.ModelForm):
    """Django form for new user registration
    
    Contains additional information not required for users to register, but can be made available for admins to see
    """
    class Meta:
        """Includes additional fields based on fields found within .models.RegisterUser
    
        Adds information needed to create a form for registrating a user using Django's admin system.

        Attributes:
            model: the Django Model the added information is based on
            exclude: a tuple of fields drawn from model to be excluded from the form
        """
        model = RegisterUser
        exclude = ('user', 'email_confirmed')

    optional_fields = ('about',)

    # Make all fields that are meant to be required, required to prevent fake account creation
    # This was done here instead of in the models to prevent existing accounts without this information
    # From being unusable, giving them a buffer window to enter the information in themselves.
    def __init__(self, *args, **kwargs):
        super(AdditionalForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            print("K"+key)
            if key not in self.optional_fields:
                print(key)
                self.fields[key].required = True

class LoginForm(forms.Form):
    """Django form for user login
    
    Contains information used to allow users to log into the CAM2 site

    Attributes:
        first_name: A CharField for the user's First Name
        last_name: A CharField for the user's Last Name
        email: An EmailField for the user's Email address

    """
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class' : 'loginput'}),required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class' : 'loginput'}), required=True)

class AppForm(forms.ModelForm):
    """Django form for API registration for an app
    
    Contains information used to register a user's app to use the CAM2 Database API

    Attributes:
        appname: A CharField for the app's name

    """
    appname = forms.CharField()

    class Meta:
        """Includes additional fields based on fields found within .models.CAM2dbApi
    
        Adds information needed to create a form for registrating an app for API use using Django's admin system.

        Attributes:
            model: the Django Model the added information is based on
            fields: a tuple of fields drawn from model to be included in the form
        """
        model = CAM2dbApi
        fields = ('appname',)

class ProfileEmailForm(forms.ModelForm):
    """Django form for changing a user's email address from the profile page
    
    Contains information for the user's email address.
    """
    class Meta:
        """Includes additional fields based on fields found within django.contrib.auth.models.User
    
        Adds information needed to create a form for changing a user's email address.

        Attributes:
            model: the Django Model the added information is based on
            fields: a tuple of fields drawn from model to be included in the form
        """
        model = User
        fields = ('email',)
    def clean_email(self):
        """Validates an email input by checking it against the database of current users
    
        Checks the email addresses of current active users and determines if the given email is in use.

        Returns:
            a cleaned version of the given email address.

        Raises:
            forms.ValidationError: the given email is associated with another user already and cannot be used again
        """
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email has already been used")
        return data

class NameForm(forms.ModelForm):
    """Django form for entering a name
    
    Contains information used to allow users to enter their name
    * Currently unused *

    Attributes:
        first_name: A CharField for the user's First Name
        last_name: A CharField for the user's Last Name
    """
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    class Meta:
        """Includes additional fields based on fields found within django.contrib.auth.models.User
    
        Adds information needed to create a form for changing a user's email address.

        Attributes:
            model: the Django Model the added information is based on
            fields: a tuple of fields drawn from model to be included in the form
        """
        model = User
        fields = ('first_name', 'last_name',)

class ReportForm(forms.Form):
    """Django form for entering information about cameras with missing images.

    Contains information used to allow users to identify a camera with a missing image. 

    Attributes:
        
    """
    cameraID = forms.CharField(required=True)
