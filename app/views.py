from django.shortcuts import render



# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from social_django.models import UserSocialAuth
from app.forms import*




# Imports for contact me page
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template




@login_required
def index(request):
    return render(request, 'app/index.html')

"""Connect the form"""
def register_page(request):
    if reguest.method == 'POST':
    	form = UserCreateForm(request.POST)
    	if form.is_valid():
        	user = user.objects.create_user(username = form.cleaned_data['username'], password = form.cleaned_data['password1'], email = form.cleaned_data['Email'], location = form.cleaned_data['Location'], occuption = form.cleaned_data['Occuption'], organization = form.cleaned_data['Organization'])
        	return HttpResponseRedirect('/')
	


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    can_disconnect = user.has_usable_password()

    return render(request, 'app/settings.html', {
        'github_login': github_login,
        'can_disconnect': can_disconnect
    })


def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
	    form = form_class(data=request.POST)

        if form.is_valid():
	        name = request.POST.get('name','')
	        email = request.POST.get('email','')
            subject = request.POST.get('subject','')
            message = request.POST.get('message','')
            template = get_template('contact_template.txt')
            context = Context({
               'name': name,
               'email': email,
               'subject': subject,
               'message': message,
            })
            content = template.render(context)

            emails = EmailMessage(
               "a new message from user",
               content,
               "Website name" + '',
               ['zzf718@gmail.com'],
               headers = {'user email': email }
            )
            emails.send()
            return redirect('contact')                  
	
    return render(request, 'contact.html', {'form': form_class,})








@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'app/password.html', {'form': form})
