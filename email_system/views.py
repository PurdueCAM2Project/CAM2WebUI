# -*- coding: utf-8 -*-
from app.models import Subteam
from django.db.models import Q
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .forms import MailForm, ContactForm, JoinForm
from .models import ContactModel, JoinModel
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mass_mail, send_mail
import os
import json
import urllib
import sys
import datetime
from django.conf import settings
from django.views.generic.edit import FormView, BaseCreateView

EMAIL_HOST_USER = settings.EMAIL_HOST_USER
MANAGER_EMAIL = settings.MANAGER_EMAIL

@staff_member_required
def admin_send_email(request):
    # obtain user id list from session, or none
    user_selected = request.session.get('user_id_selected', None)
    # get a list of User objects
    user_info=[]
    if user_selected is not None:
        for i in user_selected:
            obj=User.objects.get(id=i)
            obj_info=[obj.is_staff, obj.username, obj.email, obj.first_name, obj.last_name, obj.date_joined]
            user_info.append(obj_info)

    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            # get admin input
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            email_all_users = form.cleaned_data['email_all_users']# option for email all users

            current_site = get_current_site(request)  # will be used in templates
            try:
                if email_all_users: # if ture, send email to all users
                    all_users = User.objects.all() # For iteration of "email all users"
                    mass_email = []
                    for user in all_users:
                        if user.is_active:
                            username = user.username # will be used in template
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
                else: # send email to users in the user id list, and address that the admin typed in
                    mass_email = []
                    # for user id list
                    if user_selected is not None:
                        for i in user_selected:
                            obj = User.objects.get(id=i)
                            if obj.email is not '':
                                username = obj.username  # will be used in template
                                template = render_to_string('email_system/admin_send_email_template.html', {
                                    'username': username,
                                    'message': message,
                                    'domain': current_site.domain,
                                })
                                mass_email.append((
                                    subject,
                                    template,
                                    EMAIL_HOST_USER,
                                    [obj.email],
                                ))
                    # for additional recipient
                    for e in email:
                        """ attach template one by one to make sure only one email is in the recipient_list,
                            if not, recipients in the same recipient_list will all see the other addresses
                            in the email messages’ “To:” field """
                        username = e # will be used in template
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

                messages.success(request, 'Email successfully sent.')# success message
            except:
                messages.error(request, 'Email sent failed.')# error message

            return redirect('admin_send_email')
        else:
            messages.error(request, 'Email sent failed.')
    else:
        form = MailForm()
    return render(request, 'email_system/admin_send_email.html', {'form': form, 'users': user_info})


class ContactView(FormView):
    template_name = 'email_system/contact.html'
    model = ContactModel
    form_class = ContactForm
    success_url = 'email_sent'
    initial = {'name': '', 'from_email': '', 'subject': '', 'message': ''}
    
    def get(self, *args, **kwargs):
        try:
            self.initial['name'] = self.request.user.first_name + ' ' + self.request.user.last_name
            self.initial['from_email'] = self.request.user.email
        except:
            self.initial['name'] = ''
            self.initial['from_email'] = ''
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        #get info from form and add to email template
        subject = '[CAM2 WebUI User Feedback] ' + form.cleaned_data['subject']
        content = render_to_string('email_system/contact_email_template.html', form.cleaned_data)
        send_mail(subject, content, EMAIL_HOST_USER, [MANAGER_EMAIL])#email admin

        #add info to admin database - using cleaned_data
        contact_obj = model(date=datetime.date.today(), **form.cleaned_data)
        contact_obj.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        # Just assume. This may be a lie. I do not know.
        messages.error(self.request, 'Invalid reCAPTCHA. Please confirm you are not a robot and try again.')
        return super().form_invalid(form)

class JoinView(FormView):#BaseCreateView, 
    template_name = 'email_system/join.html'
    model = JoinModel
    form_class = JoinForm
    initial = {'name': '', 'from_email': '', 'major': '', 'courses': '', 'languages': '', 'tools': '', 'whyCAM2': '', 'anythingElse': ''}
    success_url = 'join_email_sent'
    
    def get(self, *args, **kwargs):
        try:
            self.initial['name'] = self.request.user.first_name + ' ' + self.request.user.last_name
            self.initial['from_email'] = self.request.user.email
        except:
            self.initial['name'] = ''
            self.initial['from_email'] = ''
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        #get info from form and add to email template
        subject = '[CAM2 Join Team Questions]'
        content = render_to_string('email_system/join_email_template.html', form.cleaned_data)
        email = EmailMessage(subject, content, EMAIL_HOST_USER, [MANAGER_EMAIL])
        
        file = form.cleaned_data['resume']
        file.open()
        email.attach(file.name, file.read(), file.content_type)
        file.close()
        email.send()

        #get info from form 
        data = dict(form.cleaned_data)
        del data["resume"]
        del data["captcha"]

        #add info to admin database
        join_obj = self.model(**data)
        join_obj.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(JoinView, self).get_context_data(**kwargs)
        context['subteams'] = Subteam.objects.filter(~(Q(name="None") | Q(name="Graduate Students")))
        return context
