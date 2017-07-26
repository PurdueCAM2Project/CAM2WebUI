from django.contrib import admin

# Register your models here.

from .models import FAQ, History, Publication, Team, Leader, Member, RegisterUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin #Important, dont remove
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponse
import csv


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
        

"""User Admin"""
#combine 2 model so that info from RegisterUser will be displayed with user info
class UserInline(admin.TabularInline):
    model = RegisterUser

#actions
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

def export_csv(modeladmin, request, queryset):
    #https://docs.djangoproject.com/en/1.11/howto/outputting-csv/
    #https://stackoverflow.com/questions/18685223/how-to-export-django-model-data-into-csv-file
    opts = queryset.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=CAM2UserList.csv'

    writer = csv.writer(response)
    # output field names as first row
    # required_field_names
    # ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']
    #required_field_names = [field.name for field in opts.fields] #all fields in User model
    required_field_names = ['last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']

    # optional_field_names
    # ['id', 'user', 'department', 'organization', 'title', 'country', 'about', 'email_confirmed']
    #optional_field_names = [field.name for field in RegisterUser._meta.fields] ##all fields in RegisterUser model
    optional_field_names = ['department', 'organization', 'title', 'country', 'about']

    field_names = required_field_names.copy()
    for field in optional_field_names:
        field_names.append(field)
    writer.writerow(field_names)


    # output data
    for obj in queryset:
        required_info = [getattr(obj, field) for field in required_field_names]
        try:
            optional = RegisterUser.objects.get(user=obj)  # get optional info of user
            optional_info = [getattr(optional, field) for field in optional_field_names]
        except:
            optional_info = ['N/A' for field in optional_field_names]
        for data in optional_info:
            required_info.append(data)
        writer.writerow(required_info)
    return response
download_csv.short_description = "Export selected user as csv"


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
    actions = [email_users,export_csv]

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


