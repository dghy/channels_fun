# chat/routing.py
from django.conf.urls import url

from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
]
