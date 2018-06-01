from django.contrib import admin
from .models import ContactModel, JoinModel
from django.contrib import admin

# Register your models here.

# from .models import istory, Publication, Team, Leader, Member, RegisterUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin #Important, dont remove
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponse
import csv

# Register your models here.
admin.site.register(ContactModel)
admin.site.register(JoinModel)


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'department',
        'organization',
        'title',
        'country',
        'staff_status',
        'date_joined',
    )
    # inlines = [
        # UserInline,
               # ]
    # actions = [email_users, delete_users,export_csv]

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