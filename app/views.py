from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.shortcuts import render, redirect

from social_django.models import UserSocialAuth


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from app.forms import RegistrationForm, LoginForm


def index(request):
    return render(request, 'app/index.html')

def cameras(request):
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
        print(form)
        return render(request, 'app/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

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
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)

    return render(request, 'app/profile.html', {
        'github_login': github_login,
        'can_disconnect': can_disconnect,
        'form': form,
        })

@login_required
def password(request):
    return render(request, 'app/password.html', {'form': form})
