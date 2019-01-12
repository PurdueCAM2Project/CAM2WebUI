from .models import Homepage, FAQ, History, Publication, Team, Leader, TeamMember, RegisterUser, Collab, Location, Sponsor, Poster, ReportedCamera, Calendar, Video, Subteam, Member, CAM2dbApi
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin #Important, dont remove
from django.contrib.auth.models import User
from .views.admin_actions import email_users, export_csv, report_csv, report_json
from social_django.models import Association, Nonce, UserSocialAuth

# Override Django UserAdmin class
class UserAdmin(UserAdmin):
    class UserInline(admin.StackedInline):
        model = RegisterUser
        max_num = 1
        verbose_name = "profile"
        verbose_name_plural = "additional information"
    class SocialInline(admin.TabularInline):
        model = UserSocialAuth
        readonly_fields = ('provider','uid','extra_data')
        extra = 0
        def has_add_permission(self, request, obj=None): return False
    class AppsInline(admin.TabularInline):
        model = CAM2dbApi
        verbose_name = "app"
        verbose_name_plural = "apps (might be deprecated, unsure)"
        extra = 0
    inlines = [UserInline,SocialInline,AppsInline]
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

class ReportAdmin(admin.ModelAdmin):
    actions = [report_csv, report_json]

class SubteamAdmin(admin.ModelAdmin):
    class MemberInline(admin.TabularInline):
        model = TeamMember
        extra = 0
    inlines = [MemberInline]


# Register your models here.

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Homepage)
admin.site.register(FAQ)
admin.site.register(History)
admin.site.register(Publication)
admin.site.register(Team)
admin.site.register(Sponsor)
admin.site.register(ReportedCamera, ReportAdmin)
admin.site.register(TeamMember)
admin.site.register(Poster)
admin.site.register(Video)
admin.site.register(Subteam, SubteamAdmin)

# WIP / Deprecated
# admin.site.register(Calendar)
# admin.site.register(Collab)
# admin.site.register(Member)

# Stagnant
# admin.site.register(Leader)
# admin.site.register(Location)

# Hide irrelevent Social Django models
admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
