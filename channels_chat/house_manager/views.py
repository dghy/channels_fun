# Create your views here.
from django.views.generic import TemplateView


class ControlRoom(TemplateView):
    template_name = 'house_manager/control_room.html'

