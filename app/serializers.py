from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.models import Post, PostLike


class UserActionsSerializer(serializers.ModelSerializer):
    last_activity = serializers.DateTimeField(source='actions.last_activity')

    class Meta:
        model = User
        fields = ('username', 'last_login', 'last_activity')


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source='likes_count', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'username', 'text', 'date', 'likes')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        u = User.objects.get(id=self.user.id)
        u.last_login = timezone.now()
        u.save()
        return data
