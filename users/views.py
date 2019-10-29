from rest_framework import (
    viewsets,
    mixins,
    decorators,
    response,
)
from . import (
    models, serializers
)
from authentication.serializers import LoginSerializer


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
):

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_active=True)

    def get_queryset(self):
        if self.request.method in ['PATCH', 'PUT']:
            qs = models.User.objects.filter(
                is_active=True, id=self.request.user.id
            )
        else:
            qs = super().get_queryset()
        return qs

    @decorators.action(
        methods=['GET'],
        detail=False,
        serializer_class=serializers.UserSerializer
    )
    def whoami(self, request, **kwargs):
        serializer = self.get_serializer(request.user)
        return response.Response(
            serializer.data
        )

    @decorators.action(
        methods=['POST'],
        detail=False,
        serializer_class=serializers.ChangePasswordSerializer
    )
    def change_password(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid('raise_exceptions')
        serializer.save()
        return response.Response(
            LoginSerializer(request.user).data
        )
