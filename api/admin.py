from django.contrib import admin
from django.contrib.auth.models import Group

from api import models

# Register your models here.

admin.site.unregister(Group)
admin.site.register(models.User)
admin.site.register(models.RegularUser)
admin.site.register(models.Counselor)
admin.site.register(models.Moderator)

# @admin.register(models.User)
# class UserAdmin(admin.ModelAdmin):
# 	pass