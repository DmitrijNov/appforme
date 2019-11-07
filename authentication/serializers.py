import uuid

from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt import tokens
from users import models as user_models
from core import utils
from rest_framework_simplejwt.serializers import RefreshToken, \
    TokenObtainSerializer


class CustomRefreshToken(tokens.RefreshToken):
    token_type = 'refresh'
    lifetime = jwt_serializers.api_settings.REFRESH_TOKEN_LIFETIME
    no_copy_claims = (
        jwt_serializers.api_settings.TOKEN_TYPE_CLAIM, 'exp', 'jti'
    )

    @property
    def access_token(self):
        """
        Returns an access token created from this refresh token.  Copies all
        claims present in this refresh token to the new access token except
        those claims listed in the `no_copy_claims` attribute.
        """
        access = tokens.AccessToken()

        # Use instantiation time of refresh token as relative timestamp for
        # access token "exp" claim.  This ensures that both a refresh and
        # access token expire relative to the same time if they are created as
        # a pair.
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value
        new_token, _ = tokens.OutstandingToken.objects.get_or_create(
            jti=access['jti'],
            user_id=self.payload['user_id'],
            defaults={
                'token': str(access),
                'expires_at': tokens.datetime_from_epoch(
                    access['exp']
                ),
            },
        )
        return access


class RegisterUserSerializer(serializers.ModelSerializer):

    tokens = serializers.SerializerMethodField()

    class Meta:
        model = user_models.User
        fields = (
            'email', 'full_name',  'password', 'tokens'
        )
        extra_kwargs = {
            'email': {'write_only': True},
            'full_name': {'write_only': True, 'required': True},
            'password': {'write_only': True},
            'auth_token': {'read_only': True},
        }

    @classmethod
    def get_token(cls, user):
        return CustomRefreshToken.for_user(user)

    def get_tokens(self, obj):
        data = {}
        refresh = self.get_token(obj)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    def validate_password(self, obj):
        validate_password(obj)
        return obj

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def save(self):
        password = self.validated_data.pop('password', None)
        user = super().save()
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(TokenObtainSerializer):

    tokens = serializers.SerializerMethodField()

    class Meta:
        model = user_models.User
        fields = ('email', 'password', 'tokens',)
        extra_kwargs = {
            'tokens': {
                'read_only': True
            },
            'password': {
                'write_only': True
            },
            'email': {
                'write_only': True
            }
        }

    @classmethod
    def get_token(cls, user):
        return CustomRefreshToken.for_user(user)

    def get_tokens(self, obj):
        data = {}
        refresh = self.get_token(obj)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    def validate(self, attrs):
        user = utils.get_or_none(
            user_models.User, email=attrs['email']
        )
        if user and user.check_password(attrs['password']):
            return self.get_tokens(user)
        raise serializers.ValidationError('Wrong credentials')

    def save(self):
        return self.validated_data
