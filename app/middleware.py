from django.utils import timezone

from app.models import UserActions


class UserLastActivityMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            UserActions.objects.filter(user=request.user).update(last_activity=timezone.now())

        response = self._get_response(request)
        return response
