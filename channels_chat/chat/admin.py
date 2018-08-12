from django.contrib import admin

# Register your models here.
from chat.models import ChatGroup


@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    pass
