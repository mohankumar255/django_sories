from rest_framework.serializers import Serializer,DateTimeField,ModelSerializer,ValidationError
from .models import CreatePost,CreateComment,Tags,Following,Followers
from django.contrib.auth.models import User
import uuid
from .models import CreatePost

class CommentSerializer(ModelSerializer):
    created_at = DateTimeField(format="%b %d, %Y", read_only=True)
    class Meta:
        model = CreateComment
        fields = ['comment_id', 'post', 'user', 'description', 'image_url', 'created_at']
        read_only_fields = ['comment_id', 'created_at', 'user']

    def create(self, validated_data):
        # Assign default user if not provided (you can change this to request.user)
        if "user" not in validated_data:
            validated_data["user"] = User.objects.first()  # for now, pick first user
        return super().create(validated_data)


class GETPostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    created_at = DateTimeField(format="%b %d, %Y", read_only=True)
    class Meta:
        model = CreatePost
        fields = '__all__'
        read_only_fields = ['post_id', 'created_at']  # safer


class PostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    created_at = DateTimeField(format="%b %d, %Y", read_only=True)

    class Meta:
        model = CreatePost
        fields = '__all__'
        read_only_fields = ['post_id', 'created_at']  # safer

    def create(self, validated_data):
        # Ensure post_id is always UUID
        if not validated_data.get('post_id'):
            validated_data['post_id'] = uuid.uuid4()
        # validated_data['description'] = validated_data.get('description')[:20]
        return CreatePost.objects.create(**validated_data)

    def validate_post_title(self, value):
        if len(value) < 10:
            raise ValidationError('Title is too short. Must be at least 10 characters.')
        return value

class FollowersSerializer(ModelSerializer):
    class Meta:
        model = Followers
    def create(self, validated_data):
        # validated_data['post_id'] = validated_data.get('post_id',uuid.uuid4())
        validated_data['user_id'] = validated_data.get('user_id','14356')
        followers = Followers.objects.create(**validated_data)
        return followers

class FollowingSerializer(ModelSerializer):
    class Meta:
        model = Following
    def create(self, validated_data):
        # validated_data['post_id'] = validated_data.get('post_id',uuid.uuid4())
        validated_data['user_id'] = validated_data.get('user_id','14356')
        following = Following.objects.create(**validated_data)
        return following

class SaveTagsSerializer(ModelSerializer):
    class Meta:
        model = Tags
    def create(self, validated_data):
        # validated_data['post_id'] = validated_data.get('post_id',uuid.uuid4())
        validated_data['user_id'] = validated_data.get('user_id','14356')
        following = Following.objects.create(**validated_data)
        return following
