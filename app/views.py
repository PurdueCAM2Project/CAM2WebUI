import os
import json
import urllib
import sys
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from social_django.models import UserSocialAuth
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import account_activation_token
from .forms import RegistrationForm, AdditionalForm, AppForm, ProfileEmailForm, NameForm
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from .models import FAQ, History, Publication, Team, Leader, Member, CAM2dbApi, RegisterUser
from django.http import HttpResponseNotFound

def index(request):
    return render(request, 'app/index.html')

def cameras(request):
#    context = {'google_api_key': settings.GOOGLE_API_KEY,
#               'google_client_id': settings.GOOGLE_CLIENT_ID}
    return render(request, 'app/cameras.html')

def good_cameras(request):
    return render(request, 'app/good_cameras.html')

def team(request):
    """Renders content for the Team page
    
    Retrieves information from the Team database using the matching Django Model structure.

    Args:
        request: the HttpRequest corresponding to the page to be accessed.

    Returns:
        A render that displays the page team.html, complete with information from the Team database.
    """
    team_list = Team.objects.reverse()
    leader_list = Leader.objects.reverse()
    curmember_list = Member.objects.filter(iscurrentmember=True).order_by("membername")
    oldmember_list = Member.objects.filter(iscurrentmember=False).order_by("membername")
    context = {
                "team_list": team_list,
                "leader_list": leader_list,
                "curmember_list": curmember_list,
                "oldmember_list": oldmember_list
              }
    return render(request, 'app/team.html', context)

def team_poster(request):
    return render(request, 'app/team_poster.html')

def travis_ci(request):
	return render(request, 'app/travis_ci.html')

def privacy(request):
    return render(request, 'app/privacy.html')

def terms(request):
    return render(request, 'app/terms.html')

def acknowledgement(request):
    return render(request, 'app/ack.html')

#def contact(request):
#    return render(request, 'app/contact.html')

def faqs(request):
    """Renders content for the FAQs page
    
    Retrieves information from the FAQ database using the matching Django Model structure.

    Args:
        request: the HttpRequest corresponding to the page to be accessed.

    Returns:
        A render that displays the page faq.html, complete with information from the FAQs database.
    """
    question_list = FAQ.objects.reverse()
    context = {'question_list': question_list}
    return render(request, 'app/faq.html', context)

def history(request):
    """Renders content for the History page
    
    Retrieves information from the History database using the matching Django Model structure.

    Args:
        request: the HttpRequest corresponding to the page to be accessed.

    Returns:
        A render that displays the page history.html, complete with information from the History database.
    """
    history_list = History.objects.order_by('-year', '-month')
    context = {'history_list': history_list}
    return render(request, 'app/history.html', context)

def publications(request):
    """Renders content for the Publications page
    
    Retrieves information from the Publications database using the matching Django Model structure.

    Args:
        request: the HttpRequest corresponding to the page to be accessed.

    Returns:
        A render that displays the page publications.html, complete with information from the Publications database.
    """
    publication_list = Publication.objects.reverse()
    context = {'publication_list': publication_list}
    return render(request, 'app/publications.html', context)

def advice(request):
    return render(request, 'app/advice.html')

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

def email_confirmation_sent(request):
    return render(request, 'app/email_confirmation_sent.html')

def email_confirmation_invalid(request):
    return render(request, 'app/email_confirmation_invalid.html')

def account_activated(request):
    return render(request, 'app/account_activated.html')

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

    #initialize forms
    app_form = AppForm()
    apps = CAM2dbApi.objects.filter(user=request.user).values()
    emailForm = ProfileEmailForm(instance=user)
    try:
        optional = RegisterUser.objects.get(user=user)
    except:# If cannot find RegisterUser object(social login users), create one
        add_form = AdditionalForm({})
        optional = add_form.save(commit=False)
        optional.user = user
        optional.save()
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
        'app_form': app_form,
        'apps': apps,
        'infoForm': infoForm,
        'emailForm': emailForm,
    })

""" use 'password_reset' instead
def change_password(request):
    user = request.user
    passwordform = PasswordChangeForm(user)
    if request.method == 'POST':
        passwordform = PasswordChangeForm(user, request.POST)
        if passwordform.is_valid():
            passwordform.save()
            update_session_auth_hash(request, passwordform.user)
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('profile')
        else:
            passwordform = PasswordChangeForm(user)

    return render(request, 'app/change_password.html', {'passwordform': passwordform})
"""

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
    if request.method == 'POST':
        return redirect('index')

    else:
        user = request.user
        if user.is_active:
            return redirect('index')
        else:
            try:
                github_login = user.social_auth.get(provider='github')
            except UserSocialAuth.DoesNotExist:
                github_login = None

            form2 = AdditionalForm()

            return render(request, 'app/oauthinfo.html', {'form2': form2})


def error500(request):
    return render(request, 'app/500.html')

def error404(request, exception, template_name='app/404.html'):
    return render(request, 'app/404.html')

def api_request(request):
    template_name = 'app/api_access.html'
    return render(request, template_name)


