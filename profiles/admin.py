from django.contrib import admin

from .models import *

admin.site.register(Profile)
admin.site.register(ProfileSkill)
admin.site.register(Skill)
admin.site.register(Degree)