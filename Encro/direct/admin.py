from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(OneToOneChat)
admin.site.register(GroupChat)
admin.site.register(OTOMessage)
admin.site.register(GroupMessage)
admin.site.register(GroupCall)
admin.site.register(OTOCall)