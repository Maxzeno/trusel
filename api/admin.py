from django.contrib import admin
from api.models import User, RegularUser, Counselor, Moderator

# Register your models here.

admin.site.register(User)
admin.site.register(RegularUser)
admin.site.register(Counselor)
admin.site.register(Moderator)
