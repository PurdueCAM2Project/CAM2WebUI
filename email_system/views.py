from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, render_to_response
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from email_system.forms import MailForm
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mass_mail, send_mail


#@staff_member_required
def admin_send_email(request):
    if request.method == 'POST':
        form1 = MailForm(request.POST)
        if form1.is_valid():
            model = form1.save(commit=False)
            current_site = get_current_site(request)
            #try:
            if model.email_all_users:
                all_users = User.objects.all()
                mass_email = []
                for user in all_users:
                    username = user.username
                    template = render_to_string('email_system/admin_send_email_template.html', {
                        'username': username,
                        'model': model,
                        'domain': current_site.domain,
                    })
                    mass_email.append((
                        model.subject,
                        template,
                        None,
                        [user.email],
                    ))
                send_mass_mail(mass_email)
            else:
                print(model.email)
                send_mail(model.subject,
                          model.message,
                          None,
                          [model.email])

            messages.success(request, 'Email successfully sent.')
           # except:
               # messages.error(request, 'Email sent failed.')

            return redirect('admin_send_email')
        else:
            messages.error(request, 'Email sent failed.')
    else:
        form1 = MailForm()
    return render(request, 'email_system/admin_send_email.html', {'form1': form1})


def admin_send_email_demo(request):
    if request.method == 'POST':
        form1 = MultiMailForm(request.POST)
        if form1.is_valid():
            form1.save(commit=False)
            current_site = get_current_site(request)
            #try:
            if form1.email_all_users:
                all_users = User.objects.all()
                mass_email = []
                for user in all_users:
                    username = user.username
                    template = render_to_string('email_system/admin_send_email_template.html', {
                        'username': username,
                        'model': form1,
                        'domain': current_site.domain,
                    })
                    mass_email.append((
                        form1.subject,
                        template,
                        None,
                        [user.email],
                    ))
                send_mass_mail(mass_email)
            else:
                print(form1.email)
                send_mail(form1.subject,
                          form1.message,
                          None,
                          [form1.email])

            messages.success(request, 'Email successfully sent.')
           # except:
               # messages.error(request, 'Email sent failed.')

            return redirect('admin_send_email_demo')
        else:
            messages.error(request, 'Email sent failed.')
    else:
        form1 = MailForm()
    return render(request, 'email_system/admin_send_email.html', {'form1': form1})

