from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *

class RespondentAdmin(admin.ModelAdmin):
    list_display = ('group', 'education', 'age', 'location', 'gender', 'level', 'pre_color', 'post_color', 'number','enrollment_date', 'last_update', "time_in", "time_out")

class PanasAdmin(admin.ModelAdmin):
    list_display = ('respondent','pre_post', 'question', 'answer')

admin.site.register(Respondent, RespondentAdmin)
admin.site.register(Panas, PanasAdmin)