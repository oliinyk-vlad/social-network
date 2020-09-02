from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt import views

from app.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path('auth/jwt/refresh/', views.TokenRefreshView.as_view(), name="jwt-refresh"),
    path('auth/jwt/verify/', views.TokenVerifyView.as_view(), name="jwt-verify"),

    path('', include('app.urls')),
]
