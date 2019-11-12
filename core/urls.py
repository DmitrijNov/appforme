"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('users/', include('users.urls')),
    path('chat/', include('chat.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    schema_view = get_schema_view(
            openapi.Info(
                title="Collabri API",
                default_version='v1',
                description="Collabri API",
                terms_of_service="https://www.google.com/policies/terms/",
                contact=openapi.Contact(email="contact@snippets.local"),
                license=openapi.License(name="BSD License"),
            ),
            url=settings.SWAGGER_HOST_URL,
            validators=['flex', 'ssv'],
            permission_classes=(permissions.AllowAny,),
            public=True,
        )
    urlpatterns += \
        [
            path(
                'redoc/', schema_view.with_ui('redoc', cache_timeout=None),
                name='schema-redoc'
            ),
            path('swagger/',
                 schema_view.with_ui('swagger', cache_timeout=None),
                 name='schema-swagger-ui'
                 ),
            path('docs/', include_docs_urls(title='My API title')),
            # path('silk/', include('silk.urls', namespace='silk'))
        ]
