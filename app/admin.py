from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *

class RespondentAdmin(admin.ModelAdmin):
    list_display = ('email', 'group', 'age', 'location', 'country', 'gender', 'level', 'enrollment_date', 'last_update')

class PanasAdmin(admin.ModelAdmin):
    list_display = ('respondent','pre_post', 'question', 'answer')

admin.site.register(Respondent, RespondentAdmin)
admin.site.register(Panas, PanasAdmin)