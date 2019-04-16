from ..models import Homepage, FAQ, History, Publication, Team, Faculty, TeamMember, Collab, Location, Sponsor, Poster, Calendar, Video, Member
from django.contrib.auth.models import User
from django.contrib import admin
from social_django.models import Association, Nonce, UserSocialAuth


# Name the site
admin.site.site_header = 'CAM² Website Administration'
admin.site.site_title = 'CAM² Website Administration'

# Hide irrelevent Social Django models
admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(User)

# Register your models here.
from .models import UserAdmin, ReportAdmin, SubteamAdmin
admin.site.register(Homepage)
admin.site.register(FAQ)
admin.site.register(History)
admin.site.register(Publication)
admin.site.register(Team)
admin.site.register(Sponsor)
admin.site.register(Faculty)
admin.site.register(TeamMember)
admin.site.register(Poster)
admin.site.register(Video)

# Stagnant
# admin.site.register(Location)
