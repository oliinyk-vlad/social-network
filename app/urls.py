from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('activity/', views.UserActivity.as_view()),
    path('analytics/', views.PostLikeAnalytics.as_view()),
    path('posts/<int:post_id>/<str:action>/', views.PostLikeView.as_view()),
]
