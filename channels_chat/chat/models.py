from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# create auth token for every user -> post_save signal
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class TimeStampModel(models.Model):
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.published.strftime('%y-%m-%d %H:%M:%S'))


class ChatGroup(TimeStampModel):
    admin = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.SET_NULL)
    allowed_users = models.ManyToManyField(User, related_name='chat_groups')
    name = models.CharField(max_length=255, default='Default Chat Group Name')

    def __str__(self):
        return self.name


class Message(TimeStampModel):
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup, related_name='messages',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.published.strftime('%y-%m-%d %H:%M:%S')} by {self.user}."
