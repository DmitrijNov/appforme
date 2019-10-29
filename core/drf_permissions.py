from django.conf import settings
from rest_framework.permissions import IsAuthenticated


class CORSIsAuthenticated(IsAuthenticated):

    def has_permission(self, request, view):
        return \
            (
                request.method in settings.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_active)
            )
