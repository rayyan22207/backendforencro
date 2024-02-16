from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import CustomUser, Profile,FriendRequest#,StatusModel
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Permission)