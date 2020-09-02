from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserActions(models.Model):
    user = models.OneToOneField(User, related_name='actions', on_delete=models.CASCADE)
    last_activity = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    @property
    def likes_count(self):
        return self.likes.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


@receiver(post_save, sender=User)
def create_user_actions_object(sender, instance, created, **kwargs):
    if created:
        UserActions.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_actions(sender, instance, **kwargs):
    instance.actions.save()
