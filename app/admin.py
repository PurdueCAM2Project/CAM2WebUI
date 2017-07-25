from django.contrib import admin

# Register your models here.
from django.http import HttpResponseRedirect

from .models import FAQ, History, Publication, Team, Leader, Member, RegisterUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin #Important, dont remove
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.shortcuts import render, redirect

class MemberAdmin(admin.ModelAdmin):

    list_display = ('membername', 'memberimg', 'iscurrentmember')
    actions = ['move_to_oldMember']

    def move_to_oldMember(self, request, queryset):
        rows_updated = queryset.update(memberimg=None, iscurrentmember=False)
        if rows_updated == 1:
            message_bit = "1 current member was"
        else:
            message_bit = "{0} current members were".format(rows_updated)
        self.message_user(request, "{0} successfully move to old member(s).".format(message_bit))
    move_to_oldMember.short_description = "Move Current Members to Old Members"
        

"""send user email"""
#combine 2 model so that info from RegisterUser will be displayed with user info
class UserInline(admin.TabularInline):
    model = RegisterUser

#action
def email_users(self, request, queryset):
    list = queryset.values_list('email')
    email_selected = []
    for l in list:
        email_selected.append(l)

    email_selected = str(email_selected)
    # remove empty email
    email_selected = email_selected.replace('(\'\',),', '')
    # remove redundant char
    email_selected = email_selected.replace('[', '').replace(']', '').replace('(\'', '').replace('\',)', '')

    #open a session and render the email_selected to admin_send_email view
    request.session['email_selected'] = email_selected
    return redirect('admin_send_email')
email_users.short_description = "Email Users"

#model
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'department',
        'organization',
        'title',
        'country',
        'is_staff',
        'date_joined',
    )
    inlines = [
        UserInline,
               ]
    actions = [email_users]

    # callable that display info from RegisterUser
    def department(self,user):
        return "{}".format(RegisterUser.objects.get(user=user).department)
    department.short_description = 'department'

    def organization(self,user):
        return "{}".format(RegisterUser.objects.get(user=user).organization)
    organization.short_description = 'organization'

    def title(self,user):
        return "{}".format(RegisterUser.objects.get(user=user).title)
    title.short_description = 'title'

    def country(self,user):
        return "{}".format(RegisterUser.objects.get(user=user).country)
    country.short_description = 'country'



admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(FAQ)
admin.site.register(History)
admin.site.register(Publication)
admin.site.register(Team)
admin.site.register(Leader)
admin.site.register(Member, MemberAdmin)


