from django.contrib import admin
from .models import ContactModel, JoinModel

# Register your models here.
admin.site.register(ContactModel)
admin.site.register(JoinModel)
