from django.contrib import admin

# Register your models here.
from .models import FAQ, History, Publication, Team, Leader, Member

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
        

admin.site.register(FAQ)
admin.site.register(History)
admin.site.register(Publication)
admin.site.register(Team)
admin.site.register(Leader)
admin.site.register(Member, MemberAdmin)
