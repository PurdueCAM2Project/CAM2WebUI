from django.contrib import admin

# Register your models here.


from .models import FAQ, History, Publication, Team, Leader, Member, RegisterUser, Collab, Location, Sponsor, Poster, ReportedCamera
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin #Important, dont remove
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core import serializers
import csv


class MemberAdmin(admin.ModelAdmin):

    list_display = ('membername', 'memberimg', 'iscurrentmember','subteam')
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
#combine 2 model so that info from RegisterUser can be modified inside User Admin
class UserInline(admin.TabularInline):
    model = RegisterUser

#actions
def email_users(self, request, queryset):
    list = queryset.values('email','id')

    user_id_selected = []
    for l in list:
        user_id_selected.append(l['id'])

    #open a session and render the email_selected to admin_send_email view
    request.session['user_id_selected'] = user_id_selected
    return redirect('admin_send_email')
email_users.short_description = "Email Users"

def export_csv(self, request, queryset):
    #https://docs.djangoproject.com/en/1.11/howto/outputting-csv/
    #https://stackoverflow.com/questions/18685223/how-to-export-django-model-data-into-csv-file

    #setup csv writer
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=CAM2UserList.csv'
    writer = csv.writer(response)

    #opts = queryset.model._meta
    # output field names as first row
    # required_field_names
    # ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']
    #required_field_names = [field.name for field in opts.fields] #all fields in User model
    required_field_names = ['last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']

    # optional_field_names
    # ['id', 'user', 'department', 'organization', 'title', 'country', 'about', 'email_confirmed']
    #optional_field_names = [field.name for field in RegisterUser._meta.fields] #all fields in RegisterUser model
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
            optional_info = ['' for field in optional_field_names]
        for data in optional_info:
            required_info.append(data)
        writer.writerow(required_info)
    return response
export_csv.short_description = "Export selected user as csv"

def report_csv(self, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=ReportedCameras.csv'
    writer = csv.writer(response)
    required_field_names = ['cameraID', 'reporttime']
    field_names = required_field_names.copy()
    writer.writerow(field_names)
    for obj in queryset:
        required_info = [getattr(obj, field) for field in required_field_names]
        writer.writerow(required_info)
    return response
report_csv.short_description = "Export selected cameras as csv"

def report_json(self, request, queryset):
    data = serializers.serialize("json", queryset)
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment;filename=ReportedCameras.json'
    return response
report_json.short_description = "Export selected cameras as json"


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
    inlines = [UserInline,]
    actions = [email_users,export_csv]

    def department(self, user):
        return "{}".format(RegisterUser.objects.get(user=user).department)

    department.short_description = 'department'

    def organization(self, user):
        return "{}".format(RegisterUser.objects.get(user=user).organization)

    organization.short_description = 'organization'

    def title(self, user):
        return "{}".format(RegisterUser.objects.get(user=user).title)

    title.short_description = 'title'

    def country(self, user):
        return "{}".format(RegisterUser.objects.get(user=user).country)

    country.short_description = 'country'


class ContactModel(admin.ModelAdmin):
    inlines = [UserInline,]
    actions = [email_users,export_csv]

class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'cameraID',
        'reporttime',
    )
    actions = [report_csv, report_json]
    
    def cameraID(self, cameraID):
        return "{}".format(ReportedCamera.objects.get(cameraID=cameraID).cameraID)
    cameraID.short_description = 'Camera ID'

    def reporttime(self, cameraID):
        return "{}".format(ReportedCamera.objects.get(cameraID=cameraID).reporttime)
    reporttime.short_description = 'Report Time'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(FAQ)
admin.site.register(History)
admin.site.register(Publication)
admin.site.register(Team)
admin.site.register(Leader)
admin.site.register(Collab)
admin.site.register(Sponsor)
admin.site.register(Location)
admin.site.register(ReportedCamera, ReportAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Poster)
