from django.forms import ModelForm
from curd.models import CreatePost,CreateComment


class Createpostform(ModelForm):
    class Meta:
        model = CreatePost
        fields = '__all__'


class CreateCommentform(ModelForm):
    class Meta:
        model = CreateComment
        fields = ['description','image_url']