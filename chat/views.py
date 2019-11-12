from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets,
    mixins,
    decorators,
    response,
)
from core.paginators import CustomLimitOffsetPaginator
from core import socket_utils
from . import (
    serializers, models, filters
)


class MessageViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.CreateMessageSerializer
    queryset = models.Message.objects.all().order_by(
        '-date_created'
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_class = filters.MessageFilter
    pagination_class = CustomLimitOffsetPaginator

    def get_queryset(self):
        qs = models.Message.objects.filter(
            Q(
                receiver_id=self.request.user.id
            ) |
            Q(
                sender_id=self.request.user.id
            )
        )
        return qs

    def paginate_queryset(self, queryset):
        queryset.filter(receiver_id=self.request.user.id).update(is_read=True)
        result = super().paginate_queryset(queryset)
        return result

    @decorators.action(
        methods=['POST'],
        serializer_class=serializers.CreateMessageSerializer,
        queryset=models.Message.objects.all(),
        detail=False
    )
    def create_message(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        serializer = self.get_serializer(
            data=request.data, context=context
        )
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        socket_utils.send_socket_payload(
            message.receiver_id,
            'payload',
            serializer.data
        )
        return response.Response(
            serializer.data
        )
