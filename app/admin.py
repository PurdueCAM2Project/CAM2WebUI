from django.contrib import admin

# Register your models here.
from .models import FAQ
from .models import History
from .models import Publication
from .models import Team
from .models import Leader
from .models import CurrentMember
from .models import OldMember



admin.site.register(FAQ)
admin.site.register(History)
admin.site.register(Publication)
admin.site.register(Team)
admin.site.register(Leader)
admin.site.register(CurrentMember)
admin.site.register(OldMember)

