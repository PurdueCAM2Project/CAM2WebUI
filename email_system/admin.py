import ast
from django.contrib import admin
from .models import ContactModel, JoinModel, ApplicationDeadline
from django.contrib import admin
from app.admin.actions import download_csv

# Register your models here.

# from .models import istory, Publication, Team, Leader, Member, RegisterUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin #Important, dont remove
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponse
import csv


def export_joins(self, request, queryset):  #added diff_char
    #https://docs.djangoproject.com/en/1.11/howto/outputting-csv/
    #https://stackoverflow.com/questions/18685223/how-to-export-django-model-data-into-csv-file
    
    #setup csv writer
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement;filename=CAM2JoinList.csv'
    writer = csv.writer(response)

    # replace the 'favoriteTeams' field with four individual team columns
    required_field_names = list(JoinModelAdmin.list_display)
    rf_teams = required_field_names.index('favoriteTeams')
    required_field_names[rf_teams:rf_teams+1] = ['topTeam', 'secondTeam', 'thirdTeam', 'lastTeam']

    writer.writerow(required_field_names)

    # output data
    for obj in queryset:
        required_info = []
        for field in JoinModelAdmin.list_display:
            if field == 'favoriteTeams':
                teams = getattr(obj, field)
                if teams:
                    teams = teams.split('\n')
                    del teams[5:]
                    teams += ['']*(4 - len(teams))
                else:
                    teams = ('', '', '', '')
                required_info.extend(teams)
            elif field == 'courses':
                classes = getattr(obj, field)
                try:
                    required_info.append(', '.join(ast.literal_eval(classes)))
                except:
                    required_info.append(classes)
            else:
                required_info.append(getattr(obj, field))
        writer.writerow(required_info)
    return response
export_joins.short_description = "Export selected %(verbose_name_plural)s as csv"

class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_email', 'subject','message', 'date')
    actions = [download_csv]

class JoinModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_email', 'major', 'gradDate', 'favoriteTeams', 'courses', 'languages', 'knowledge', 'teamwork', 'problem', 'futureLeader', 'whyCAM2', 'anythingElse', 'date')
    actions = [export_joins]



# Register your models here.
admin.site.register(ContactModel, ContactModelAdmin)
admin.site.register(JoinModel, JoinModelAdmin)
admin.site.register(ApplicationDeadline)
