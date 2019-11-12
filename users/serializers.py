from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from . import models
from core.base64_serializer import Base64ImageField
from core.utils import get_or_none
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'initial_data') and self.initial_data.get('avatar') \
                and (
                self.initial_data.get('avatar').startswith('http') or
                self.initial_data.get('avatar').startswith('/')
        ):
            self.initial_data.pop('avatar')
    avatar = Base64ImageField(required=True)

    class Meta:
        model = models.User
        fields = (
            'id', 'email', 'full_name', 'avatar'
        )
        extra_kwargs = {
            'full_name': {
                'allow_blank': False,
                'allow_null': False
            }
        }


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        max_length=255
    )
    new_password = serializers.CharField(
        validators=[
            validate_password
        ]
    )

    def validate_current_password(self, obj):
        if not self.context['request'].user.check_password(
            obj
        ):
            raise serializers.ValidationError(
                'Wrong password'
            )
        return obj

    def validate(self, attrs):
        if attrs['current_password'] == attrs['new_password']:
            raise serializers.ValidationError(
                'Passwords cannot be the same'
            )
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        key = user.auth_token
        t = get_or_none(Token, key=key)
        if t:
            t.delete()
        user.set_password(
            validated_data['new_password']
        )
        Token.objects.create(user=user)
        user.save()
        return user


class SimpleUserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=True)

    class Meta:
        model = models.User
        ref_name = None
        fields = (
            'id', 'email', 'full_name', 'avatar'
        )
        extra_kwargs = {
            'employee_rate': {
                'read_only': True
            },
            'helper_rate': {
                'read_only': True
            }
        }
