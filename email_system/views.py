from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from cam2webui.settings import EMAIL_HOST_USER, MANAGER_EMAIL
from email_system.forms import MailForm, ContactForm
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mass_mail, send_mail

@staff_member_required
def admin_send_email(request):
    email_table = (User.objects.values('email').order_by('date_joined')) #Obtaining a list of users' emails outside users info table for easy copying and pasting.
    users = User.objects.values_list('username', 'first_name', 'last_name', 'date_joined').order_by('date_joined') #Obtaining a list of info required from user
    #obtain email selected by admin from session, or none
    email_selected = request.session.get('email_selected', None)
    if email_selected == None:
        email_selected = ''
    #email_selected = request.session['email_selected']
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            #get admin input
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            email_all_users = form.cleaned_data['email_all_users']#option for email all users

            current_site = get_current_site(request)  # will be used in templates
            try:
                if email_all_users: #if ture, send email to all users
                    all_users = User.objects.all() #For iteration of "email all users"
                    mass_email = []
                    for user in all_users:
                        if user.is_active:
                            username = user.username #will be used in template
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
                    send_mass_mail(mass_email, fail_silently=False)
                else: #if email_all_users is False, send email to address that the admin typed in
                    mass_email = []
                    for e in email: #attach template one by one to make sure only one email shows up in the recipient list,
                                    #if not, recipients in the same recipient_list will all see the other addresses in the email messages’ “To:” field
                        username = e #will be used in template
                        template = render_to_string('email_system/admin_send_email_template.html', {
                            'username': username,
                            'message': message,
                            'domain': current_site.domain,
                        })
                        mass_email.append((
                            subject,
                            template,
                            EMAIL_HOST_USER,
                            [e],
                        ))
                    send_mass_mail(mass_email, fail_silently=False)

                messages.success(request, 'Email successfully sent.')#success message
            except:
                messages.error(request, 'Email sent failed.')#error message

            return redirect('admin_send_email')
        else:
            messages.error(request, 'Email sent failed.')
    else:
        form = MailForm()
    return render(request, 'email_system/admin_send_email.html', {'form': form, 'users': users, 'email_table': email_table, 'email_selected': email_selected,})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            #get info from form
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['from_email']
            subject = '[CAM2 WebUI User Feedback] ' + form.cleaned_data['subject']
            message = form.cleaned_data['message']
            #add info to email template
            content = render_to_string('email_system/contact_email_template.html', {
                'name': name,
                'from_email': from_email,
                'message': message,
            })
            send_mail(subject, content, EMAIL_HOST_USER, MANAGER_EMAIL)#email admin

            return redirect('email_sent')
    else:
        form = ContactForm()
    return render(request, "email_system/contact.html", {'form': form})

def email_sent(request):
    return render(request, 'email_system/email_sent.html')
