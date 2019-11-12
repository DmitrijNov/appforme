from rest_framework import serializers
from . import models
from core.base64_serializer import CustomBase64FileField


class MessageAttachmentSerializer(serializers.ModelSerializer):
    file = CustomBase64FileField()

    class Meta:
        model = models.MessageAttachment
        fields = (
            'file',
        )


class CreateMessageSerializer(serializers.ModelSerializer):

    attachments = MessageAttachmentSerializer(
        many=True, allow_null=True, required=False
    )

    class Meta:
        model = models.Message
        fields = (
            'id', 'text', 'receiver', 'sender', 'attachments'
        )
        extra_kwargs = {
            'sender': {
                'read_only': True
            },
            'type': {
                'read_only': True
            },
            'notification_type': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        validated_data['sender_id'] = self.context['request'].user.id
        attachments = validated_data.pop('attachments', [])
        message = super().create(validated_data)
        if attachments:
            [a.setdefault('message_id', message.id) for a in attachments]
            MessageAttachmentSerializer(many=True).create(
                attachments
            )

        return message


class MessageSerializer(serializers.ModelSerializer):
    attachments = MessageAttachmentSerializer(many=True, allow_null=True)

    class Meta:
        model = models.Message
        fields = (
            'id', 'text', 'is_read', 'receiver', 'sender',
            'attachments', 'date_created'
        )
