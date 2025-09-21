from django.urls import path
from .views import (Createcomment,userlist,getsinglepost,deletepost,bulkdatacreation,
                    save_tags,CreatePostView,get_all_categories,get_all_stories_by_author)
urlpatterns = [
    # path('get_data11',get_data),
    #path('create_post',create_post),
    #path('single_post/<str:pk>',get_single_post),
    path('create_post/',CreatePostView.as_view()),
    path('get_data/',userlist.as_view()),
    path('post/<str:post_id>/',getsinglepost.as_view()),
    path('delete_post/<str:post_id>/', deletepost.as_view()),
    path('bulk_create/',bulkdatacreation.as_view()),
    path('create_comment/<uuid:post_id>', Createcomment.as_view()),
    path('tags/<str:post_id>/<str:tag_name>',save_tags),
    path('categories/', get_all_categories),
    path('author/<str:author>', get_all_stories_by_author),

]