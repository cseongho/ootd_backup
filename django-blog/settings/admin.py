from django.contrib import admin
from .models import Setting

# Register your models here.

class SettingAdmin(admin.ModelAdmin):
	list_display = ('title', 'email', 'facebook', 'instagram', 'youtube', 'left_credit', 'right_credit')
	save_on_top = True
	search_fields = ['title', 'email', 'left_credit', 'right_credit']

admin.site.register(Setting, SettingAdmin)