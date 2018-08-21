from django.contrib import admin

from chat.models import ChatGroup

# admin.autodiscover()
# # remove default user and group from admin panel
# admin.site.unregister(User)
# admin.site.unregister(Group)
from house_manager.models import ScheduledEvent


@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(ScheduledEvent)
class ScheduledEventAdmin(admin.ModelAdmin):
    pass
