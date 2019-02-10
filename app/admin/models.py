from ..models import TeamMember, RegisterUser, ReportedCamera, Subteam, CAM2dbApi
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin #Important, dont remove
from django.contrib.auth.models import User
from .actions import email_users, export_csv, report_csv, report_json
from social_django.models import UserSocialAuth

# Override Django UserAdmin class
@admin.register(User)
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

@admin.register(ReportedCamera)
class ReportAdmin(admin.ModelAdmin):
    actions = [report_csv, report_json]

@admin.register(Subteam)
class SubteamAdmin(admin.ModelAdmin):
    class MemberInline(admin.TabularInline):
        model = TeamMember
        extra = 0
    inlines = [MemberInline]
