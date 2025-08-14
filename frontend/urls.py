from tkinter.font import names

from django.urls import path
from .views import feed,home,create_post,get_data_tags,delete_post,loginapiview,get_single_post


urlpatterns = [path('',home,name='home'),
               path('feed/', feed, name='showfeed'),
               path('create_post/', create_post, name='create_post'),
               #path('show_feed/',   get_data_ob,name = 'showfeed'),
               path('tags_name/<str:pk>/<str:tag_name>/',get_data_tags , name = 'tags_name'),
               path('delete_post/<str:pk>/',delete_post,name='delete_post'),
               path('login/', loginapiview),
               path('view_single_post/<str:pk>',get_single_post,name = 'view_single_post'),
               ]
