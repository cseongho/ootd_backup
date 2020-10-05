from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    save_on_top = True
    search_fields = ['user']

admin.site.register(Profile, ProfileAdmin)
