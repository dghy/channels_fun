# chat/views.py
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import ListView, TemplateView

from chat.models import ChatGroup


class ActionManager(LoginRequiredMixin, TemplateView):
    template_name = 'manager.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(kwargs)
        # TODO: MAKE LIST OF ALL SUBMODULES OF THE APP
        links = dict()
        context.update(links=links)
        return context


class AllowedChatGroups(LoginRequiredMixin, ListView):
    """Display possible chat groups for the logged user"""
    model = ChatGroup
    template_name = 'chat/index.html'

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
        context = super().get_context_data(**kwargs)
        context.update(room_name_json=mark_safe(json.dumps(kwargs['room_id'])))
        return context
