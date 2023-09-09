from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from accounts.models import UserProfile
from .models import Post


@receiver(post_save, sender=Post)
def update_user_post_count_on_save(instance, sender: Post, **kwargs):
    posts = Post.objects.filter(user=instance.user).count()
    UserProfile.objects.filter(user=instance.user).update(post=posts)


@receiver(post_delete, sender=Post)
def update_user_post_count_on_delete(instance, sender: Post, **kwargs):
    posts = Post.objects.filter(user=instance.user).count()
    UserProfile.objects.filter(user=instance.user).update(post=posts)
