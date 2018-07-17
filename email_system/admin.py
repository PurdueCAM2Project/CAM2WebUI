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


def export_csv1(self, request, queryset):
    #https://docs.djangoproject.com/en/1.11/howto/outputting-csv/
    #https://stackoverflow.com/questions/18685223/how-to-export-django-model-data-into-csv-file
    
    #setup csv writer
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement;filename=CAM2ContactList.csv'
    writer = csv.writer(response)
    
    #opts = queryset.model._meta
    # output field names as first row
    # required_field_names
    # ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']
    # required_field_names = queryset #all fields in User model
	
    required_field_names = ['name', 'from_email', 'subject', 'message', 'date']

    # optional_field_names
    # ['id', 'user', 'department', 'organization', 'title', 'country', 'about', 'email_confirmed']
    #optional_field_names = [field.name for field in RegisterUser._meta.fields] #all fields in RegisterUser model
	
	
    
	#optional_field_names = ['department', 'organization', 'title', 'country', 'about']

    field_names = required_field_names.copy()
    writer.writerow(field_names)


    # output data
    for obj in queryset:
        required_info = [getattr(obj, field) for field in required_field_names]
        writer.writerow(required_info)
    return response
export_csv1.short_description = "Export selected user as csv"


def export_csv(self, request, queryset):  #added diff_char
    #https://docs.djangoproject.com/en/1.11/howto/outputting-csv/
    #https://stackoverflow.com/questions/18685223/how-to-export-django-model-data-into-csv-file
    
    #setup csv writer
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement;filename=CAM2JoinList.csv'
    writer = csv.writer(response)
    
    #opts = queryset.model._meta
    # output field names as first row
    # required_field_names
    # ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']
    # required_field_names = queryset #all fields in User model
	
    required_field_names = ['name', 'from_email', 'major', 'gradDate','courses', 'languages', 'tools', 'whyCAM2', 'anythingElse', 'date']

    # optional_field_names
    # ['id', 'user', 'department', 'organization', 'title', 'country', 'about', 'email_confirmed']
    #optional_field_names = [field.name for field in RegisterUser._meta.fields] #all fields in RegisterUser model
	
	
    # optional_field_names = ['department', 'organization', 'title', 'country', 'about']

    field_names = required_field_names.copy()
    # for field in optional_field_names:
        # field_names.append(field)
    writer.writerow(field_names)


    # output data
    for obj in queryset:
        required_info = [getattr(obj, field) for field in required_field_names]
        # try:
            # optional = RegisterUser.objects.get(user=obj)  # get optional info of user
            # optional_info = [getattr(optional, field) for field in optional_field_names]
        # except:
            # optional_info = ['' for field in optional_field_names]
        # for data in optional_info:
            # required_info.append(data)
        writer.writerow(required_info)
    return response
export_csv.short_description = "Export selected user as csv"

class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_email', 'subject','message', 'date')
    actions = [export_csv1]
	

class JoinModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_email', 'major', 'gradDate','courses', 'languages', 'tools', 'whyCAM2', 'anythingElse', 'date')
    actions = [export_csv]


	
	




# Register your models here.
admin.site.register(ContactModel, ContactModelAdmin)
admin.site.register(JoinModel, JoinModelAdmin)
#admin.site.register()