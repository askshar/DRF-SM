from config.base import BaseModel
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    image = models.ImageField(upload_to='posts/', default='img.png')
    caption = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    liked_by = models.ManyToManyField(User, related_name='likes', null=True, blank=True)

    def __str__(self):
        return f"Post by {self.user.username}"
    

class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    comment = models.CharField(max_length=500)

    def __str__(self):
        return self.comment
