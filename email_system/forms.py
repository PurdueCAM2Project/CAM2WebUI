from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import requests
from .models import ContactModel, JoinModel
from .validators import GraduationValidator

class MultiEmailField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        #Modify the input so that email can be split by , and ;
        #For copying and pasting email address from the list, None, () \ will be removed.
        value = value.replace(' ', '')
        value = value.replace('None,', '')
        value = value.replace(';', ',')
        value = value.replace(',,', ',')
        print(value)
        while value.endswith(',') or value.endswith(';'):
            value = value[:-1] #remove the last ',' or ';'

        return value.split(',')

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)
        for email in value:
            validate_email(email)

class ReCaptchaWidget(forms.widgets.Widget):
    """Used to link the ReCaptchaField class to the HTML markup."""
    template_name = "recaptcha.html"

    def __init__(self, api_params=None, *args, **kwargs):
        super(ReCaptchaWidget, self).__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        return data.get("g-recaptcha-response", None)

class ReCaptchaField(forms.CharField):
    """Use this field to add a ReCAPTCHA to a form. To enable, add the following code to your form.

    captcha = ReCaptchaField()
    """
    widget = ReCaptchaWidget

    def __init__(self, *args, **kwargs):
        super(ReCaptchaField, self).__init__(*args, **kwargs)
        self.required = True
        self.widget.attrs["data-sitekey"] = settings.RECAPTCHA_SITE_KEY

    def validate(self, value):
        super(ReCaptchaField, self).validate(value)

        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': value
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if not result['success']:
            raise ValidationError(
                'Invalid reCAPTCHA. Please try again.',
                code="captcha_invalid"
            )

class MailForm(forms.Form):
    email = MultiEmailField(label='Email of Additional Recipient', required=False, help_text='Split email by " ,  " or " ; ", or copy paste a list from below')
    email_all_users = forms.BooleanField(required=False, help_text='Checking this box will not send email to additional recipient')
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)

class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    captcha = ReCaptchaField()

class JoinForm(forms.ModelForm):
    class Meta:

        # Options to be used in the programming classes field
        PROGRAMMING_CLASSES = (
          ("CS314", "CS 314 - Numerical Methods"),
          ("Computer Science", (
            ("CS180", "CS 180 - Problem Solving And Object-Oriented Programming"),
            ("CS182", "CS 182 - Foundations of Computer Science"),
            ("CS240", "CS 240 - C Programming"),
            ("CS251", "CS 251 - Data Structures And Algorithms"),
            ("CS252", "CS 252 - Systems Programming"),
            ("CS348", "CS 348 - Information Systems"),
            ("CS307", "CS 307 - Software Engineering I"),
            ("CS373", "CS 373 - Data Mining & Machine Learning"),
            ("CS381", "CS 381 - Introduction to Analysis of Algorithms"),
            ("CS407", "CS 407 - Software Engineering II"),
            ("CS490", "CS 490 - Artificial Neural Network & Deep Architectures"),
          )),
          ("Engineering", (
            ("CS159", "CS 159 - Programming Applications For Engineers"),
            ("ECE264", "ECE 264 - Advanced Programming in C"),
            ("ECE270", "ECE 270 - Introduction To Digital System Design"),
            ("ECE30862", "ECE 30862 - Object-Oriented Programming in C++ and Java"),
            ("ECE364", "ECE 364 - Software Engineering Tools Laboratory"),
            ("ECE368", "ECE 368 - Data Structures"),
            ("ECE461", "ECE 461 - Software Engineering"),
            ("ENGR132", "ENGR 132 - Transforming Ideas to Innovation II"),
            ("MA366", "MA 366 - Ordinary Differential Equations"),
          )),
        )

        # Use all of the fields from the JoinModel to generate the form
        model = JoinModel

        # The date will be automatically set to the submission date
        exclude = ("date",)

        # Use more user-friendly widgets
        widgets = {
            'major': forms.TextInput(attrs={"list":"majors", "placeholder":"CS,CmpE,etc."}),
            'courses': forms.SelectMultiple(choices=PROGRAMMING_CLASSES, attrs={"class":"form-control"}),
            'favoriteTeams': forms.Textarea(attrs={"class":"textarea-lg", "rows":"", "placeholder":"(most wanted at the top)\r\n\r\nActive Learning\r\nTransfer Learning\r\nCamera Database API and Discovery\r\nCamera Reliability\r\n\r\n(least wanted at the bottom)\r\n"}),
            'languages': forms.Textarea(attrs={"class":"textarea-lg", "rows":"", "placeholder":"C: 3\r\nJava: 3\r\nPython: 5\r\nShell: 2\r\n"}),
            'knowledge': forms.Textarea(attrs={"class":"textarea-lg", "rows":"", "placeholder":"machine learning and deep learning theory: 4\r\nmachine learning and deep learning software: 2\r\ncomputer vision: 1\r\n"}), # , "placeholder":"PLACEHOLDER\r\n"
            'teamwork': forms.Textarea(attrs={"class":"textarea-lg", "rows":""}),
            'problem': forms.Textarea(attrs={"class":"textarea-lg", "rows":""}),
            'futureLeader': forms.CheckboxInput(attrs={"style":"width:auto;"}),
            'whyCAM2': forms.Textarea(attrs={"class":"textarea-lg", "rows":"", "placeholder":"Just a couple sentences will suffice.\r\n"}),
            'anythingElse': forms.Textarea(attrs={"class":"textarea-lg", "rows":"", "placeholder":"Clarify anything you want about your survey answers.\r\n"}),
        }

    # Add a resume field which will be attached to the email instead of being added to the database.
    resume = forms.FileField(widget=forms.FileInput(attrs={"accept":".pdf, application/pdf"}), required=True)
    captcha = ReCaptchaField()

    def clean_resume(self):
        """Tests if the resume is in a PDF file."""
        resume = self.cleaned_data['resume']
        if resume.content_type != 'application/pdf':
            raise ValidationError("File is not a PDF.")
        return resume

