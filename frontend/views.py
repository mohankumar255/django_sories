import json
import jwt
import math
from django.shortcuts import render,redirect
from envs.black.DLLs.unicodedata import category
from rest_framework.response import Response
from django.template.response import TemplateResponse
from .forms import Createpostform,CreateCommentform
import  requests
from new_api.constan_data import page_size
from curd.models import CreatePost,User
# Create your views here.
from django.http import HttpResponse
local_url = 'http://127.0.0.1:8000/'
like_json_file = 'media/likes_json_data.json'


headers = {
    'Authorization': ''}

#
# def login():
#     user_name = 'mohan'
#     password = '1234'
#     data = requests.request(method='post',url=local_url+'token',data = {
#     "username": user_name,
#     "password": password
# })
#     print(data)
# login()


def get_all_cat(cat_name=None):
    data = requests.request('get','http://127.0.0.1:8000/api/v1/categories/')
    cat_data = data.json()
    catgeries ={url:url.replace(' ','-') for url in cat_data}
    return catgeries

def home(request):
    return TemplateResponse(request , 'home.html',{'catgeries':get_all_cat()})
def create_post(request):
    form_data = Createpostform(request.POST or None, request.FILES or None)
    headers['Authorization'] = 'Bearer ' + loginapiview({'username': 'mohan', 'password': '1234'})['access']

    if request.method == 'POST':
        if form_data.is_valid():
            request_data = form_data.cleaned_data

            # ✅ Handle image properly
            files = {}
            if "image" in request.FILES:
                files["image"] = request.FILES["image"]

            # Remove csrf token if present
            request_data.pop("csrfmiddlewaretoken", None)
            request_data.pop("image", None)  # remove image field from normal data

            print("Files being sent:", files)
            print("Data being sent:", request_data)

            # ✅ Post to API (multipart/form-data)
            api_data = requests.post(
                url=local_url + 'api/v1/create_post/',
                headers=headers,   # don’t set Content-Type
                data=request_data, # text fields
                files=files        # file field
            )

            api_response = api_data.json()
            print("API Response:", api_response)

            return redirect(f"/view_single_post/{api_response['post_id']}")

    return TemplateResponse(request, 'create_post.html', {
        'data': form_data,
        'catgeries': get_all_cat()
    })

from django.core.paginator import Paginator

def feed_1(request):
    posts = CreatePost.objects.all().order_by('-created_at')  # Adjust ordering as needed
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    catgeries = get_all_cat()
    return render(request, 'feed.html', {'page_obj': page_obj,'catgeries':catgeries})


def update_data():
    pass

def feed(request):
    page_num = request.GET.get('page',None)
    category = request.GET.get('category',None)
    page_num_url = f'/?page={page_num}' if page_num else ''
    category_url = f'category={category}' if category else ''
    category_url = '&'+category_url if page_num_url else '/?'+category_url
    api_data = requests.request('get',f'http://127.0.0.1:8000/api/v1/get_data{page_num_url}{category_url}')
    print(api_data.url,"====")
    data = api_data.json()
    last_page = math.ceil(data['count']/page_size)
    # previous = data['previous'].split('page=')[1] if data['previous'] else None
    current = int(page_num) if page_num else page_num
    if not current:
        current = 1
    previous = current-1 if data['previous'] else None
    next = current+1 if data['next'] else None
    get_all_cat_data = get_all_cat()
    feed_data = data['results']
    for i in feed_data:
        i['post_id'] = str(i['post_id']).replace('-','')
    like_json_file = 'media/likes_json_data.json'
    file_data = open(like_json_file,'r')
    read_data= file_data.read()
    json_data = json.loads(read_data)
    for i in feed_data[5:10]:
        i['description'] = i['description'][:10]
        if json_data.get(str(i['post_id']),None):
            i['likes'] = json_data[str(i['post_id'])]
    return TemplateResponse(request,'feed.html',{'posts':feed_data,'catgeries':get_all_cat_data,'current':current,'next':next,'previous':previous,'last_page':last_page,'category':category})

def get_data_tags(request , pk,tag_name):
    data = requests.request(url=local_url + f'api/v1/tags/{pk}/{tag_name}', method='get')
    if data.status_code==401:
        headers['Authorization'] = 'Bearer ' + loginapiview({'username': 'mohan', 'password': '1234'})['access']
        data = requests.request(url=local_url + f'api/v1/tags/{pk}/{tag_name}', method='get')
    return redirect('/feed/')


def delete_post(request, pk):
    data = requests.request(url=local_url + f'api/v1/delete_post/{pk}/', method='delete')
    return redirect('/feed/')

def loginapiview(data):
    request_data = requests.request(method='post',url=local_url+'token/',data=data)
    return request_data.json()
def get_single_post(request,pk):
    catgeries = get_all_cat()
    data = requests.request(url=local_url + f'api/v1/post/{pk}/', method='get',headers=headers)
    if data.status_code == 401:
        headers['Authorization'] = 'Bearer ' + loginapiview({'username': 'mohan', 'password': '1234'})['access']
        data = requests.request(url=local_url + f'api/v1/post/{pk}/', method='get',headers=headers)
    json_data = data.json()
    post_id = str(json_data['post_id'])
    # title= str(json_data['post_title']+'.txt')
    story_read_data = open(rf"C:\Users\mk302\Downloads\content_creater\all_stories\{post_id}.txt",'r',encoding='utf-8')
    read_data = story_read_data.read()
    story_read_data.close()
    return render(request, 'individual_post.html', {'post': json_data,'read_story':read_data,'catgeries':catgeries})
    #return render(request,'individual_post.html',{'post':data.json()})

def get_name_change(request,pk):

    data = requests.request(url=local_url + f'api/v1/post/{pk}/', method='get', headers=headers)
    if data.status_code == 401:
        headers['Authorization'] = 'Bearer ' + loginapiview({'username': 'mohan', 'password': '1234'})['access']
        data = requests.request(url=local_url + f'api/v1/post/{pk}/', method='get', headers=headers)
    json_data = data.json()
    print(json_data)
    title = str(json_data['post_title'] + '.txt')
    story_read_data = open(rf"C:\Users\mk302\PycharmProjects\content_creater\all_stories\{title}", 'r',
                           encoding='utf-8')
    read_data = story_read_data.read()
    story_read_data.close()

def login(request):
    username = request.POST['username']
    password = request.POST['password']

