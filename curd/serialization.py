from rest_framework.serializers import Serializer,ModelSerializer,ValidationError
from .models import CreatePost,CreateComment,Tags,Following,Followers
import uuid


class CommentSerializer(ModelSerializer):
    class Meta:
        model = CreateComment
        fields = ['description','image_url','post','user']
        read_only_fields = ['post_id','user_id']

    def create(self, validated_data):
        #validated_data['comment_id'] = validated_data.get('comment_id',uuid.uuid4())
        print(validated_data)
        validated_data['user_id'] = validated_data.get('user_id',1)
        comment = CreateComment.objects.create(**validated_data)

        return comment


class PostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = CreatePost
        fields = '__all__'
        # fields = ['user','comments','post_id','created_at','post_title','description','image_url']
        # read_only_fields = ['post_id']
    def create(self, validated_data):
        validated_data['post_id'] = validated_data.get('post_id',uuid.uuid4())
        post = CreatePost.objects.create(**validated_data)
        return post
        #CreatePost.save(**validated_data)
    def validate_post_title(self,value):
        if len(value)<10:
            raise ValidationError('Title is too short.')
        else:
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
