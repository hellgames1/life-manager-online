from django.contrib import admin

# Register your models here.
from .models import Day, UserSettings
admin.site.register(Day)
admin.site.register(UserSettings)