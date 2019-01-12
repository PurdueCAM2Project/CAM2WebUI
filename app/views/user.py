from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from django.core.mail import mail_admins, send_mail
from social_django.models import UserSocialAuth
from ..tokens import account_activation_token
from ..forms import RegistrationForm, AdditionalForm, AppForm, ProfileEmailForm, NameForm
from ..models import CAM2dbApi, RegisterUser
import sys
import os
import urllib
import requests
import json

def register(request):
    """Renders content for the Registration form page

    Uses the Django Forms structure outlined in forms.py to create a form for users to use
    to register their information. When the user submits this form, it validates it to ensure
    that the values are acceptable and that the required fields were filled, then it stores
    the contents of the form into the Django Admin database for Users. Once this is complete,
    an email is sent to the provided email address that contains an activation link for the user
    to click.

    Args:
        request: the HttpRequest corresponding to the page to be accessed or the submitted form.

    Returns:
        A render that displays the form page if the page was just accessed or the form was invalid,
        or a redirection to a page that confirms that the account was registered.
    """
    if request.method == 'POST':
        form1 = RegistrationForm(request.POST)
        form2 = AdditionalForm(request.POST)


        if form1.is_valid() and form2.is_valid():

            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if result['success']:
                model1 = form1.save(commit=False) #Required information of user
                model1.is_active = False #Set true for testing without email.
                model1.save()
                model2 = form2.save(commit=False) #Optional information of user
                model2.user = model1
                model2.save()

                #Email user
                current_site = get_current_site(request)
                subject = 'Activate Your CAM2 Account'
                message = render_to_string('app/confirmation_email.html', {
                    'user': model1,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(model1.pk)).decode(),
                    'token': account_activation_token.make_token(model1),
                })
                model1.email_user(subject, message)

                return redirect('email_confirmation_sent')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please confirm you are not a robot and try again.')
                if 'test' in sys.argv:
                    sitekey = os.environ['RECAPTCHA_TEST_SITE_KEY']
                else:
                    sitekey = os.environ['RECAPTCHA_SITE_KEY']
        else:
            if 'test' in sys.argv:
                sitekey = os.environ['RECAPTCHA_TEST_SITE_KEY']
            else:
                sitekey = os.environ['RECAPTCHA_SITE_KEY']
    else:
        form1 = RegistrationForm()
        form2 = AdditionalForm()
        if 'test' in sys.argv:
            sitekey = os.environ['RECAPTCHA_TEST_SITE_KEY']
        else:
            sitekey = os.environ['RECAPTCHA_SITE_KEY']

    return render(request, 'app/register.html', {'form1': form1, 'form2': form2, 'sitekey': sitekey})

def activate(request, uidb64, token):
    """Renders content for account activation

    Determines which user is attempting to activate their account based on the encoded section of the
    URL used to access the page, sets the user's account to an activated state and saves the change
    to the database, emails the system administrator about the newly registered account, logs the user
    in, and redirects them to the site.

    Args:
        request: the HttpRequest corresponding to the page to be accessed.
        uidb64: an encoded form of the user id used in activation.
        token: the access token for activation given by the activation link.

    Returns:
        Either a redirection to the site indicating successful confirmation, or a rendering of a page
        that indicates a failure to activate the account.
    """
    """Followed tutorial: https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html"""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.registeruser.email_confirmed = True
        user.save()

        optional = RegisterUser.objects.get(user=user) #get optional info of user
        #email admin
        admin_subject = 'New User Registered'
        admin_message = render_to_string('app/new_user_email_to_admin.html', {
            'user': user,
            'optional': optional,
        })


        mail_admins(admin_subject, admin_message)
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect('account_activated')
    else:
        return render(request, 'email_confirmation_invalid.html')

@login_required
def profile(request):
    """Renders content for the Profile page

    For a user that's currently logged in, displays information currently stored in the database
    for that user (First Name, Last Name, email, etc...), and allows the User to modify that
    information using a form.

    Also pulls information provided by Github sign-in, if Github authentication was used to access
    the site.

    Args:
        request: the HttpRequest corresponding to the page to be accessed.

    Returns:
        A render that displays the user's profile page, complete with all information accessible from the
        Django admin database for that specific user.
    """
    user = request.user
    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    #initialize forms
    app_form = AppForm()
    apps = CAM2dbApi.objects.filter(user=request.user).values()
    emailForm = ProfileEmailForm(instance=user)
    try:
        optional = RegisterUser.objects.get(user=user)
    except:# If cannot find RegisterUser object(social login users), create one
        return redirect('/oauthinfo')
    infoForm = AdditionalForm(instance=optional)#get form with info of a specific instance


    '''
    # Enter name for social login users
    if request.method == 'POST' and 'saveName' in request.POST:
        nameForm = NameForm(request.POST, instance=user)
        if nameForm.is_valid():
            nameForm.save()
            messages.success(request, 'Thank you! Your name has been updated.')
        else:
            nameForm = NameForm(instance=user)
            messages.error(request, 'Something went wrong. Please try again or contact us!')
        #return redirect('profile')
    return render(request, 'app/profile.html', form_dict)
    '''
    # Add app
    if request.method == 'POST' and 'add' in request.POST:
        app_form = AppForm(request.POST)
        if app_form.is_valid():
            dbapp = app_form.save(commit=False)
            dbapp.user = request.user
            dbapp.save()
            return redirect('profile')
    else:
        app_form = AppForm()
        #messages.error(request, 'Something went wrong. Please try again or contact us!')
    #return render(request, 'app/profile.html', form_dict)

    # Change Email
    if request.method == 'POST' and 'changeEmail' in request.POST:
        emailForm = ProfileEmailForm(request.POST, instance=user)
        if emailForm.is_valid():
            emailForm.save()
            messages.success(request, 'Your Email has been successfully updated!')
            return redirect('profile')
    else:
        emailForm=ProfileEmailForm(instance=user)
        #messages.error(request, 'Something went wrong. Please try again or contact us!')
    #return render(request, 'app/profile.html', form_dict)

    # Modify Profile
    if request.method == 'POST' and 'changeInfo' in request.POST:
        infoForm = AdditionalForm(request.POST, instance=optional)
        if infoForm.is_valid():
            infoForm.save()
            messages.success(request, 'Your information has been successfully updated!')
            return redirect('profile')
    else:
        infoForm=AdditionalForm(instance=optional)
        #messages.error(request, 'Something went wrong. Please try again or contact us!')
    return render(request, 'app/profile.html', {
        'github_login': github_login,
        'google_login': google_login,
        'app_form': app_form,
        'apps': apps,
        'infoForm': infoForm,
        'emailForm': emailForm,
    })

@login_required
def oauthinfo(request):
    """Renders a form for additional content for users authenticated with Github or Google

    Retrieves information from the social authentication library provided by Django and allows
    a user authenticated with an external service to provide additional information about themselves
    (organization, location, etc...) that can then be stored within the Django admin user database.

    * Note that while this appears to be the intention, it isn't fully implemented yet *

    Args:
        request: the HttpRequest corresponding to the page to be accessed.

    Returns:
        A render that displays the page for externally authenticated users to add information about themselves.
    """
    user = request.user

    if request.method == 'POST':
        form = AdditionalForm(request.POST, request.FILES)
        if form.is_valid():
            save_it = form.save(commit = False)
            save_it.user = user
            save_it.save()
            return redirect('index')
        else:
            return render(request, 'app/oauthinfo.html', {'form2': form})

    else:
        try:
            optional = RegisterUser.objects.get(user=user)
            return redirect('index')
        except:# If cannot find RegisterUser object(social login users), create one
            form2 = AdditionalForm()

            return render(request, 'app/oauthinfo.html', {'form2': form2})
