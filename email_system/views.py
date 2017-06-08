from itertools import chain

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, render_to_response
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from app.models import RegisterUser
from email_system.forms import MailForm
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mass_mail, send_mail

#@staff_member_required
def admin_send_email(request):
    email_table = list(User.objects.values_list('email'))

    #email_table = email_table.join(', ')
    users = User.objects.values_list('username', 'first_name', 'last_name')
    u = User.objects.all()
    re = RegisterUser.objects.all()

    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            email_all_users = form.cleaned_data['email_all_users']
            current_site = get_current_site(request)
            all_users = User.objects.all()
            #try:
            if email_all_users:

                mass_email = []
                for user in all_users:
                    username = user.username
                    template = render_to_string('email_system/admin_send_email_template.html', {
                        'username': username,
                        'message': message,
                        'domain': current_site.domain,
                    })
                    mass_email.append((
                        subject,
                        template,
                        None,
                        [user.email],
                    ))
                send_mass_mail(mass_email)
            else:
                print(email)
                send_mail(subject,message,None,email)

            messages.success(request, 'Email successfully sent.')
           # except:
               # messages.error(request, 'Email sent failed.')

            return redirect('admin_send_email')
        else:
            messages.error(request, 'Email sent failed.')
    else:
        form = MailForm()
    return render(request, 'email_system/admin_send_email.html', {'form': form, 'users': users, 'email_table': email_table})

def extract_email(email_table):
    email_table = [e.replace('(','') for e in email_table]
    #print(email_table)
    #email_table = re.sub('(,)', '', email_table)
    #email_table = re.replace(',', '', email_table)
    #email_table = re.replace(')', '', email_table)
    return email_table
