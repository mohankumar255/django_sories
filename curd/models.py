import datetime

from django.db import models
import uuid
from django.contrib.auth.models import User


# Create your models here.
class CreatePost(models.Model):
    user_name = models.CharField(default='Mohan')
    #id = models.CharField(default=uuid.uuid4())
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    post_title = models.CharField(max_length=100)
    description = models.TextField()
    models.DateTimeField(auto_now_add=True)
    #image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    image_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post title {0}'.format(self.post_title)

class CreateComment(models.Model):
    models.DateTimeField(auto_now_add=True)
    comment_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(CreatePost,on_delete=models.CASCADE,related_name='comments')
    description = models.TextField()
    image_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment ID {0}'.format(self.comment_id)

class Tag_choices(models.Choices):
    defaul_tag = 'Like'
    negative_tag = 'Deslike'


class Tags(models.Model):
    user = models.CharField(max_length=100)
    like_tag = models.TextField(Tag_choices.choices)
    comment = models.ForeignKey(CreatePost,on_delete=models.CASCADE)
class Followers(models.Model):
    follower = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)
class Following(models.Model):
    user= models.CharField(max_length=100)
    follower = models.ForeignKey(User,on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

