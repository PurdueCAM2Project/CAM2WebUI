import csv
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect

def email_users(self, request, queryset):
    """This admin action emails users who are selected in the admin window"""
    list = queryset.values('email','id')

    #get ids of currently selected users
    user_id_selected = [l['id'] for l in list]

    #open a session and render the email_selected to admin_send_email view
    request.session['user_id_selected'] = user_id_selected
    return redirect('admin_send_email')
email_users.short_description = "Email Users"

def export_users(self, request, queryset):
    """This admin action serializes the selected user objects into a csv file

    For the more general case, use download_csv instead
    """
    #https://docs.djangoproject.com/en/1.11/howto/outputting-csv/
    #https://stackoverflow.com/questions/18685223/how-to-export-django-model-data-into-csv-file

    # This line is put here to make this actions module more general and usable elsewhere
    from ..models import RegisterUser

    #setup csv writer
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=CAM2UserList.csv'
    writer = csv.writer(response)

    # required_field_names
    #required_field_names = [field.name for field in queryset.model._meta.fields] #all fields in User model
    required_field_names = ['last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']

    # optional_field_names
    #optional_field_names = [field.name for field in RegisterUser._meta.fields] #all fields in RegisterUser model
    optional_field_names = ['department', 'organization', 'title', 'country', 'about']

    # merge both required and optional fields together and output field names as first row
    field_names = [*required_field_names, *optional_field_names]
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
export_users.short_description = "Export selected %(verbose_name_plural)s as csv"

def download_csv(self, request, queryset):
    """This admin action serializes the selected objects into a csv file"""
    #https://docs.djangoproject.com/en/1.11/howto/outputting-csv/
    #https://stackoverflow.com/questions/18685223/how-to-export-django-model-data-into-csv-file

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename='+str(queryset.model.__name__)+'s.csv'
    writer = csv.writer(response)
    field_names = [field.name for field in queryset.model._meta.fields]
    writer.writerow(field_names)
    for obj in queryset:
        required_info = [getattr(obj, field) for field in field_names]
        writer.writerow(required_info)
    return response
download_csv.short_description = "Export selected %(verbose_name_plural)s as csv"

def download_json(self, request, queryset):
    """This admin action serializes the selected objects into a json file"""
    data = serializers.serialize("json", queryset)
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = 'attachment;filename='+str(queryset.model.__name__)+'s.json'
    return response
download_json.short_description = "Export selected %(verbose_name_plural)s as json"
