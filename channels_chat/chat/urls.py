# chat/urls.py
from django.urls import path

from chat.views import AllowedChatGroups, RoomView

urlpatterns = [
    path('', AllowedChatGroups.as_view(), name='select_chat'),
    path('<int:room_id>/', RoomView.as_view(), name='chat'),
]
