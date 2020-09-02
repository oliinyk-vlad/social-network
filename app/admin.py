from django.contrib import admin

from app.models import UserActions, Post, PostLike


@admin.register(UserActions)
class UserActionsAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    pass
