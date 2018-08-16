from rest_framework import serializers

from chat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)

    class Meta:
        model = Message
        read_only_fields = ('published', 'username',)
        fields = ('text', 'published', 'username', 'user', 'group')

    def create(self, validated_data):
        return Message.objects.create(**validated_data)
