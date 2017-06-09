from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from cam2webui.settings import EMAIL_HOST_USER
from email_system.forms import MailForm
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mass_mail, send_mail

#@staff_member_required
def admin_send_email(request):
    email_table = (User.objects.values('email'))
    users = User.objects.values_list('username', 'first_name', 'last_name', 'date_joined')
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            email_all_users = form.cleaned_data['email_all_users']
            current_site = get_current_site(request)
            all_users = User.objects.all()
            try:
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
                            EMAIL_HOST_USER,
                            [user.email],
                        ))
                    send_mass_mail(mass_email)
                else:
                    send_mail(subject,message,EMAIL_HOST_USER,email)

                messages.success(request, 'Email successfully sent.')
            except:
                messages.error(request, 'Email sent failed.')

            return redirect('admin_send_email')
        else:
            messages.error(request, 'Email sent failed.')
    else:
        form = MailForm()
    return render(request, 'email_system/admin_send_email.html', {'form': form, 'users': users, 'email_table': email_table})
