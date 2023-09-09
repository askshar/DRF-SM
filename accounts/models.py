from config.base import BaseModel
from django.db import models
from django.contrib.auth.models import User


class UserPasswordHistoryMananger(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recent_password')
    password = models.CharField(max_length=155, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Password History Manager"


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile/', default='img.png')
    post = models.IntegerField(default=0)
    follower = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'User Profile'


class UserConfig(BaseModel):
    """
    This model will be used in many user related utilities.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_config')
    token = models.CharField(max_length=250, null=True, blank=True)
    generation_time = models.DateTimeField(null=True)

    def __str__(self):
        if self.token:
            return self.token
        return self.user.username

    class Meta:
        verbose_name_plural = "User Configuration"
