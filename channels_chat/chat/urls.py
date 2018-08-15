# chat/urls.py
from django.urls import path

from chat.views import AllowedChatGroups, RoomView, AddUserToChatView

urlpatterns = [
    path('', AllowedChatGroups.as_view(), name='select_chat'),
    path('<int:room_id>/', RoomView.as_view(), name='chat'),
    # path('add_user', AddUserView.as_view(), name='add_user')
    path('add_user_to_chat/<int:pk>', AddUserToChatView.as_view(),
         name='add_user_to_chat')
]
