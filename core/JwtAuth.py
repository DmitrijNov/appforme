from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from rest_framework_simplejwt.utils import aware_utcnow
from rest_framework_simplejwt import tokens
from django.utils.translation import ugettext_lazy as _
from users.models import User
from core.utils import get_or_none


class CustomJwtAuth(tokens.BlacklistMixin, AccessToken):
    def __init__(self, token=None, verify=True):
        self.token = token
        self.current_time = aware_utcnow()
        if token is not None:
            # An encoded token was provided
            from rest_framework_simplejwt.state import token_backend

            # Decode token
            try:
                self.payload = token_backend.decode(token, verify=verify)
                if not get_or_none(User, pk=self.payload['user_id']):
                    raise TokenError(_('Token is invalid or expired'))
            except TokenBackendError:
                raise TokenError(_('Token is invalid or expired'))
            if tokens.BlacklistedToken.objects.filter(
                token__jti=self.payload['jti']
            ).exists():
                raise TokenError(_('Token is blacklisted'))
            if verify:
                self.verify()
                new_token, created = \
                    tokens.OutstandingToken.objects.get_or_create(
                        jti=self.payload['jti'],
                        user_id=self.payload['user_id'],
                        defaults={
                            'token': str(self.token),
                            'expires_at': tokens.datetime_from_epoch(
                                self.payload['exp']
                            ),
                        },
                    )
        super().__init__(token, verify)
