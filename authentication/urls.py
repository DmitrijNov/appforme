from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views

app_name = 'auth'

urlpatterns = [
    path(
        'login/', views.LoginView.as_view()
    ),
    path(
        'register/', views.RegisterView.as_view()
    ),
    path('token/refresh/', TokenRefreshView.as_view()),
]
