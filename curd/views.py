import json
from django.db import transaction

from .models import User
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from rest_framework.response import Response
from  rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import CreatePost,CreateComment,Following,Followers,Tags
from .serialization import PostSerializer,CommentSerializer,SaveTagsSerializer,FollowersSerializer,FollowingSerializer
# Create your views here.
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly
from .pagination import PaginationClass
from rest_framework.renderers import TemplateHTMLRenderer
like_json_file = 'media/likes_json_data.json'
#
# @api_view(['GET'])
# def get_data(request):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'home.html'
#     data = CreatePost.objects.all()
#     # data = PostSerializer(data=data,many=True)
#     # print(data.is_valid())
#     # if data.is_valid():
#     return Response({"name":"mohan"})
#
# @api_view(['POST'])
# def create_post(request):
#     data = request.data
#     serializer = PostSerializer( data = data)
#     if serializer.is_valid():
#         serializer.save()
#
#     return Response(f"post create with title {serializer.data}")
#
# @api_view(['GET'])
# def get_single_post(request,pk):
#     single_data = CreatePost.objects.get(post_id = pk)
#     data = PostSerializer(data = single_data)
#     if data.is_valid():
#         return Response(data.data)
#     return Response(data.errors)


class userlist(generics.ListAPIView):
    queryset = CreatePost.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = PaginationClass

    def get_queryset(self):
        queryset = CreatePost.objects.all()
        # Get query params
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset
    #filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price']  # Exact match filtering
    search_fields = ['name', 'description']  # Full-text search
class getsinglepost(generics.RetrieveAPIView):
    queryset = CreatePost.objects.prefetch_related('comments')
    lookup_field = 'post_id'
    serializer_class = PostSerializer
class deletepost(generics.DestroyAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = CreatePost.objects.all()
    lookup_field = 'post_id'
    serializer_class = PostSerializer

class bulkdatacreation(generics.ListCreateAPIView):
    with transaction.atomic():
        queryset = CreatePost.objects.all()
        serializer_class = PostSerializer
        def create(self, request, *args, **kwargs):
            is_many = isinstance(request.data,list)
            serilizer = self.get_serializer(data = request.data,many=is_many)
            serilizer.is_valid(raise_exception = True)
            self.perform_create(serilizer)
            return Response(serilizer.data)
        def perform_create(self, serializer):
            serializer.save()




class Createcomment(generics.CreateAPIView):
    queryset = CreateComment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'post_id'
    def create(self, request, *args, **kwargs):
        #is_many = isinstance(request.data,list)
        serilizer = self.get_serializer(data = request.data)
        serilizer.is_valid(raise_exception = True)
        self.perform_create(serilizer)
        return Response(serilizer.data)
    def perform_create(self, serializer):
        serializer.save()
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class CreatePostView(generics.CreateAPIView):
    queryset = CreatePost.objects.all()
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    # permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get validated data safely
        post_title = serializer.validated_data.get('post_title')
        description = serializer.validated_data.get('description')
        image_file = serializer.validated_data.get('image')

        if image_file:
            post_instance= serializer.save(image=image_file)
        else:
            post_instance = serializer.save()
        post_id = str(post_instance.post_id)
        # Sanitize file name
        safe_title = "".join(c for c in post_title if c.isalnum() or c in (" ", "-", "_")).rstrip()
        file_path = rf"C:\Users\mk302\Downloads\content_creater\all_stories\{post_id}.txt"

        # Write description to file
        with open(file_path, 'w', encoding='utf-8') as story_file:
            description = description.replace('\r\n', '\n').replace('\r', '\n')
            story_file.write(description)
        return Response(serializer.data)

#
# class CreatePostView(generics.CreateAPIView):
#     queryset = CreateComment.objects.all()
#     serializer_class = PostSerializer
#     # permission_classes = [IsAuthenticated]
#     def create(self, request, *args, **kwargs):
#         serilizer = self.get_serializer(data = request.data)
#         serilizer.is_valid(raise_exception = True)
#         self.perform_create(serilizer)
#         return Response(serilizer.data)
#     def perform_create(self, serializer):
#         serializer.save()

class GetPost(generics.RetrieveAPIView):
    queryset = CreateComment.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = ['post_id']
    def create(self, request, *args, **kwargs):
        serilizer = self.get_serializer(data = request.data)
        serilizer.is_valid(raise_exception = True)
        self.perform_create(serilizer)
        return Response(serilizer.data)
    def perform_create(self, serializer):
        serializer.save()


@api_view(['GET'])
def save_tags(request, post_id, tag_name):
    post_id = str(post_id)
    if True:
        filedata = open(like_json_file,'r')
        data = filedata.read()
        data = json.loads(data)
        if data and data.get(post_id,None):
            if tag_name not in data[post_id]:
                data[post_id][tag_name] =1
            else:
                data[post_id][tag_name] = data[post_id][tag_name]+1
        else:
            data[post_id] = {tag_name:1}
        filedata.close()
    write_data = open(like_json_file, 'w')
    data = json.dumps(data)
    write_data.write(data)
    write_data.close()
    return Response(data)

@api_view(['GET'])
def get_all_categories(request):
    queryset = CreatePost.objects.all()
    data = {key.category:key.category for key in queryset}
    return Response(data)
