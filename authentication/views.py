from rest_framework import (
    response,
    generics,
    permissions
)
from users import models as user_models
from rest_framework_simplejwt.views import TokenViewBase
from . import (
    serializers
)


class LoginView(TokenViewBase):
    serializer_class = serializers.LoginSerializer
    queryset = user_models.User.objects.all()
    permission_classes = (permissions.AllowAny,)


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
