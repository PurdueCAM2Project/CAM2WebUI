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

def index(request):
    return render(request, 'app/index.html')

def watch(request):
    return render(request, 'app/watch.html')

def cameras(request):
#    context = {'google_api_key': settings.GOOGLE_API_KEY,
#               'google_client_id': settings.GOOGLE_CLIENT_ID}
    return render(request, 'app/cameras.html')

def team(request):
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

def privacy(request):
    return render(request, 'app/privacy.html')

def terms(request):
    return render(request, 'app/terms.html')

def acknowledgement(request):
    return render(request, 'app/ack.html')

#def contact(request):
#    return render(request, 'app/contact.html')

def faqs(request):
    question_list = FAQ.objects.reverse()
    context = {'question_list': question_list}
    return render(request, 'app/faq.html', context)

def history(request):
    history_list = History.objects.order_by('-year', '-month')
    context = {'history_list': history_list}
    return render(request, 'app/history.html', context)

def publications(request):
    publication_list = Publication.objects.reverse()
    context = {'publication_list': publication_list}
    return render(request, 'app/publications.html', context)

def register(request):
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
                model1.is_active = True #Set true for testing without email.
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
                    'uid': urlsafe_base64_encode(force_bytes(model1.pk)),
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
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    # Enter name for social login users
    nameForm = NameForm(instance=user)

    if request.method == 'POST' and 'saveName' in request.POST:
        nameForm = NameForm(request.POST, instance=user)
        if nameForm.is_valid():
            nameForm.save()
            messages.success(request, 'Thank you! Your name has been updated.')
        else:
            nameForm = NameForm(instance=user)
            messages.error(request, 'Something went wrong. Please try again or contact us!')
        return redirect('profile')


    # Add app
    app_form = AppForm()

    apps = CAM2dbApi.objects.filter(user=request.user).values()

    if request.method == 'POST' and 'add' in request.POST:
        app_form = AppForm(request.POST)
        if app_form.is_valid():
            dbapp = app_form.save(commit=False)
            dbapp.user = request.user
            dbapp.save()
        return redirect('profile')

    # Change Email
    emailForm = ProfileEmailForm(instance=user)

    if request.method == 'POST' and 'changeEmail' in request.POST:
        emailForm = ProfileEmailForm(request.POST, instance=user)
        if emailForm.is_valid():
            emailForm.save()
            messages.success(request, 'Your Email has been successfully updated!')
        else:
            emailForm=ProfileEmailForm(instance=user)
            messages.error(request, 'Something went wrong. Please try again or contact us!')
        return redirect('profile')

    # Modify Profile
    try:
        optional = RegisterUser.objects.get(user=user)
    except:# If cannot find RegisterUser object(social login users), create one
        add_form = AdditionalForm({})
        optional = add_form.save(commit=False)
        optional.user = user
        optional.save()
    infoForm = AdditionalForm(instance=optional)#get form with info of a specific instance

    if request.method == 'POST' and 'changeInfo' in request.POST:
        infoForm = AdditionalForm(request.POST, instance=optional)
        if infoForm.is_valid():
            infoForm.save()
            messages.success(request, 'Your information has been successfully updated!')
        else:
            infoForm=AdditionalForm(instance=optional)
            messages.error(request, 'Something went wrong. Please try again or contact us!')
        return redirect('profile')

    return render(request, 'app/profile.html', {
        'github_login': github_login,
        'app_form': app_form,
        'apps': apps,
        'infoForm': infoForm,
        'emailForm': emailForm,
        'nameForm': nameForm
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

def error404(request):
    return render(request, 'app/404.html')
