from django.http import Http404
from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response

from chat.models import Message, CustomUser, ChatGroup
from rest_api.serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    # http_method_names = ('GET', 'POST', 'HEAD', 'OPTIONS')
    lookup_field = 'user__username'
    http_method_names = ('get', 'post', 'options', 'head')

    # permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        user = get_object_or_404(CustomUser,
                                 username=self.kwargs['user__username'])
        queryset = Message.objects.filter(user=user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = Message.objects.filter(user=request.user)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        return self.list(request)

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)
        data = dict([(key, value) for key, value in request.data.items()])

        data.setdefault('text')
        data.setdefault('group')

        if not data['group'].isdigit():
            raise Http404('ChatGroup ID should be given as integer.')
        group = get_object_or_404(ChatGroup, id=data['group'])
        data = dict(text=data['text'],
                    user=user.id,
                    group=group)

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            Message.objects.create(**serializer.validated_data)
            return Response({'message': 'Message POSTED'},
                            status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Message could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
