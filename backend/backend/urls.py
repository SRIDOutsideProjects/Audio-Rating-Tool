"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include

# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from django.conf import settings
from django.conf.urls.static import static


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)

schema_view = get_schema_view(
    openapi.Info(
        title="Audio Annotation API",
        default_version="v1",
        description="Test description",
        contact=openapi.Contact(email="pk20pankajjha@gmail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)
admin.site.site_header = "Audio Annotation API Administration"
admin.site.site_title = "Audio Annotation API"
admin.site.index_title = "Administration Panel"

urlpatterns = [
    # path('auth/obtain_token_pair/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # # Submit your refresh token to this path to obtain a new access token
    # path('auth/refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',include('authentication.urls')),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),
    path("rest/", include("rest_framework.urls", namespace="rest_framework")),
    path("accounts/", include("django.contrib.auth.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

