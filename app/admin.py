from django.contrib import admin

from .models import FAQs
# Register your models here.

admin.site.register(FAQs)
admin.site.register(History)
admin.site.register(Publication)
admin.site.register(Team)
admin.site.register(Leader)
admin.site.register(CurrentMember)
admin.site.register(OldMember)

