from rest_framework import viewsets, mixins, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models.functions import TruncDay
from django.db.models import Count

from rest_framework_simplejwt.views import TokenObtainPairView

from app.common import validate_date_format
from app.models import Post, PostLike
from app.serializers import UserActionsSerializer, PostSerializer, CustomTokenObtainPairSerializer


class UserActivity(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserActionsSerializer(request.user)
        return Response(data=serializer.data)


class PostViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.order_by('-date')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostLikeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, **kwargs):
        try:
            return PostLike.objects.get(**kwargs)
        except PostLike.DoesNotExist:
            return

    def post(self, request, post_id, action, *args, **kwargs):
        post_like = self.get_object(post=post_id, user=request.user)

        if action == 'like':
            if not post_like:
                PostLike.objects.create(post_id=post_id, user=request.user)
                return Response(status=status.HTTP_200_OK)
        elif action == 'unlike':
            if post_like:
                post_like.delete()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostLikeAnalytics(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        if date_from and date_to:
            try:
                validate_date_format(date_from)
                validate_date_format(date_to)
            except ValueError as e:
                return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            data = PostLike.objects.filter(date__range=(date_from, date_to)).annotate(
                day=TruncDay('date')).values("day").annotate(likes=Count('id')).order_by("-day")
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
