from django.urls import path

from house_manager.views import ControlRoom

urlpatterns = [
    path('', ControlRoom.as_view(), name='control_room')
]
