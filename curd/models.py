import datetime

from django.db import models
import uuid
from django.contrib.auth.models import User

import uuid
from django.db import models
from django.contrib.auth.models import User
import os

def post_image_upload(instance, filename):
    # get file extension (.jpg, .png etc.)
    ext = filename.split('.')[-1]
    # rename file to post_id.ext
    filename = f"{instance.post_id}.{ext}"
    # save in 'uploads/' folder
    return os.path.join("uploads", filename)
class CreatePost(models.Model):
    email = models.CharField(max_length=100, default='Mohan')
    category = models.CharField(max_length=50, default='sex kathalu')
    post_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    post_title = models.CharField(max_length=100)
    description = models.TextField()

    # Use ImageField instead of URLField
    image = models.ImageField(upload_to=post_image_upload, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post title: {self.post_title}"

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

