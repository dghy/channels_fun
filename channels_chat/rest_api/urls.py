# .. Imports
from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from rest_api.views import MessageViewSet

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet, base_name='messages')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^', include(router.urls))
]
