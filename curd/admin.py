from django.contrib import admin
from .models import CreatePost,CreateComment,Tags,Following,Followers
admin.site.register(CreatePost)
admin.site.register(CreateComment)
admin.site.register(Tags)
admin.site.register(Following)
admin.site.register(Followers)

# Register your models here.
