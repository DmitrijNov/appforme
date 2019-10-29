from rest_framework import (
    response,
    generics,
    permissions
)
from users import models as user_models
from . import (
    serializers
)
from collections import OrderedDict

class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    queryset = user_models.User.objects.filter(is_active=True)
    permission_classes = (permissions.AllowAny,)

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data
        )


class RegisterView(generics.GenericAPIView):
    serializer_class = serializers.RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)
    model = user_models.User

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data
        )
