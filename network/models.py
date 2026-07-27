from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    
class Follow(models.Model):
    #followers, followings
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following1')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower1')
      
    
class Post (models.Model):
    post_content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, related_name="likepost")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="likeuser")