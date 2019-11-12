from django.urls import path, include

from rest_framework import routers

from . import views

app_name = 'chat'

router = routers.SimpleRouter()
router.register('messages', views.MessageViewSet)

urlpatterns = [
    path(
        '', include(router.urls),
    ),
]
