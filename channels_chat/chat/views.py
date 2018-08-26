# chat/views.py
import json
from time import sleep


from gpiozero import LED

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import RedirectView
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import ListView, TemplateView, CreateView, UpdateView

from chat.forms import AddUserToChatForm
from chat.models import ChatGroup, Message, User

# GPIO 17 on Raspberry3 board
red = LED(17)



class ActionManager(LoginRequiredMixin, TemplateView):
    template_name = 'manager.html'


class AllowedChatGroups(LoginRequiredMixin, ListView):
    """Display possible chat groups for the logged user"""
    model = ChatGroup
    template_name = 'chat/chat_rooms.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(allowed_users=self.request.user)

    def get_context_data(self, object_list=None, **kwargs):
        content_type = ContentType.objects.get_for_model(self.model)
        context = super().get_context_data()
        chat_groups_urls = [(group.id,
                             reverse("%s" % content_type.app_label,
                                     args=(group.id,)))
                            for group in context['chatgroup_list']]
        context.update(chatgroup_urls=dict(chat_groups_urls))
        return context


class RoomView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        room_id = mark_safe(json.dumps(kwargs['room_id']))
        messages = Message.objects.filter(group_id=room_id).order_by('-published')[:15]
        # TODO: use serializer?
        users = json.dumps(list(User.objects.filter(chat_groups__id__in=room_id).values_list('username')))
        messages_json = \
            json.dumps(dict(map(
                lambda x: (x.id, (x.text, x.user.username, x.published.strftime('%y-%m-%d %H:%M:%S'))),
                messages)))

        context = super().get_context_data(**kwargs)
        context.update(room_name_json=room_id, messages=messages_json,
                       users=users)
        return context


class AddUserToChatView(LoginRequiredMixin, UpdateView):
    template_name = 'chat/add_user_to_chat_template.html'
    form_class = AddUserToChatForm
    success_url = reverse_lazy('select_chat')

    def get_queryset(self):
        chat_id = str(self.kwargs['pk'])
        if not chat_id.isdigit():
            raise Http404
        return ChatGroup.objects.filter(id=chat_id)


class CreateChatGroup(LoginRequiredMixin, CreateView):
    model = ChatGroup
    success_url = reverse_lazy('select_chat')
    fields = '__all__'
    template_name = 'chat/create_chat.html'


# class AddUserView(LoginRequiredMixin, CreateView):
#     template_name = 'chat/add_user_form_template.html'
#     form_class = AddUserToChatForm
#     success_url = reverse_lazy('select_chat')


class ToggleLight(LoginRequiredMixin, RedirectView):
    http_method_names = ['get', 'head', 'option']
    url = reverse_lazy('manager')

    def get(self, request, *args, **kwargs):

        print(red.is_active, type(red.is_active))
        if not red.is_active:
            red.on()
        else:
            red.off()
        return redirect('manager')

