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


class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_email', 'subject','message', 'date')
	

class JoinModelAdmin(admin.ModelAdmin):
    st_display = ('name', 'from_email', 'major', 'gradDate','courses', 'languages', 'tools', 'whyCAM2', 'anythingElse', 'date')




# Register your models here.
admin.site.register(ContactModel, ContactModelAdmin)
admin.site.register(JoinModel, )
#admin.site.register()