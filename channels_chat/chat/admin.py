from django.contrib import admin

# Register your models here.
# from django.contrib.auth.models import User, Group

from chat.models import ChatGroup, CustomUser

# admin.autodiscover()
# # remove default user and group from admin panel
# admin.site.unregister(User)
# admin.site.unregister(Group)


@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    pass
