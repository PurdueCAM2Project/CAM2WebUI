from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect

from social_django.models import UserSocialAuth

from cam2webui import urls
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
#from django.contrib.auth.forms import UserCreationForm
from app.forms import RegistrationForm, AdditionalForm, LoginForm


def index(request):
    return render(request, 'app/index.html')

def cameras(request):
    context = {'google_api_key': settings.GOOGLE_API_KEY,
               'google_client_id': settings.GOOGLE_CLIENT_ID}
    return render(request, 'app/cameras.html')

def team(request):
    return render(request, 'app/team.html')

def privacy(request):
    return render(request, 'app/privacy.html')

def terms(request):
    return render(request, 'app/terms.html')

def acknowledgement(request):
    return render(request, 'app/ack.html')

def contact(request):
    return render(request, 'app/contact.html')

def faqs(request):
    return render(request, 'app/faq.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        else:
            print("invalid form")

        return render(request, 'app/profile.html')
    else:
        form = LoginForm()
        return render(request, 'app/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form1 = RegistrationForm(request.POST)
        form2 = AdditionalForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            model1 = form1.save()
            model2 = form2.save(commit=False)
            model2.user = model1
            model2.save()
            username = form1.cleaned_data.get('username')
            raw_password = form1.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)#should always be true, just check
            return redirect('index')
    else:
        form1 = RegistrationForm()
        form2 = AdditionalForm()
    return render(request, 'app/register.html', {'form1': form1, 'form2': form2})

@login_required
def profile(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    can_disconnect = user.has_usable_password()

    if can_disconnect:
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
    else:
        form = PasswordForm(request.user)

    return render(request, 'app/profile.html', {
        'github_login': github_login,
        'can_disconnect': can_disconnect,
        'form': form,
        })
"""
@login_required
def password(request):
    return render(request, 'app/password.html', {'form': form})
"""
