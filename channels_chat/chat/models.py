from django.contrib.auth.models import User
from django.db import models


class TimeStampModel(models.Model):
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.published


class ChatGroup(TimeStampModel):
    admin = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.SET_NULL)
    allowed_users = models.ManyToManyField(User, related_name='users')
    name = models.CharField(max_length=255, default='Default Chat Group Name')

    def __str__(self):
        return self.name


class Message(TimeStampModel):
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup, related_name='messages',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f"Message: published {self.published} by {self.user}."

