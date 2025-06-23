import json
import jwt

from django.shortcuts import render,redirect
from rest_framework.response import Response
from django.template.response import TemplateResponse
from .forms import Createpostform,CreateCommentform
import  requests
from curd.models import CreatePost,User
# Create your views here.
from django.http import HttpResponse
local_url = 'http://127.0.0.1:8000/'
like_json_file = 'media/likes_json_data.json'


headers = {
    'Authorization': '',
    'Content-Type': 'application/json',
}


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

    read_file = open('..\content_creater\links.json', 'r')
    data = json.loads(read_file.read())
    all_urls = []
    links_data = data

    for i in links_data:
        all_urls+=links_data[i]
    if cat_name:
        selected_urls = [url for url in all_urls if '/'+cat_name.replace(' ','-').lower()+'/' in url]

        return selected_urls
    categorys = list(set([url.replace('https://www.kamakathalu.com/','').split('/')[0].replace('-',' ').title() for url in all_urls]))
    return categorys

def home(request):
    return TemplateResponse(request , 'home.html')

def create_post(request):
    form_data = Createpostform(request.POST)
    headers['Authorization']='Bearer '+loginapiview({'username':'mohan','password':'1234'})['access']
    if request.method =='POST':
        if form_data.is_valid():
            request_data = form_data.data.dict()
            request_data['user'] = int(request_data['user'])
            del request_data['csrfmiddlewaretoken']
            api_data = requests.request(url=local_url+'api/v1/create_post/',
                    headers=headers,method='post',data=(json.dumps(request_data)))
            api_response = api_data.json()
            data = open(like_json_file, 'r')
            read_data = data.read()
            data.close()
            read_data = json.loads(read_data)
            read_data[api_response['post_id']] = {'likes': 0, 'dislikes': 0}
            data = open(like_json_file, 'w')
            read_data = json.dumps(read_data)
            write_data = data.write(read_data)
            data.close()
            return redirect('/show_feed/')
    return TemplateResponse(request,'create_post.html',{'data':form_data})

def get_data_ob(request):
    data = CreatePost.objects.all()
    get_all_cat_data = get_all_cat()
    catgeries ={url:url.replace(' ','-') for url in get_all_cat_data}

    for i in data:
        i.post_id = str(i.post_id).replace('-','')
    like_json_file = 'media/likes_json_data.json'
    file_data = open(like_json_file,'r')
    read_data= file_data.read()
    json_data = json.loads(read_data)
    for i in data:
        i.description = i.description[:10]
        if json_data.get(str(i.post_id),None):
            i.likes = json_data[str(i.post_id)]
    return TemplateResponse(request,'feed.html',{'posts':data,'categories':get_all_cat_data})

def get_data_tags(request , pk,tag_name):
    data = requests.request(url=local_url + f'api/v1/tags/{pk}/{tag_name}', method='get')
    if data.status_code==401:
        headers['Authorization'] = 'Bearer ' + loginapiview({'username': 'mohan', 'password': '1234'})['access']
        data = requests.request(url=local_url + f'api/v1/tags/{pk}/{tag_name}', method='get')
    return redirect('/show_feed/')


def delete_post(request, pk):
    data = requests.request(url=local_url + f'api/v1/delete_post/{pk}/', method='delete')
    return redirect('/show_feed/')

def loginapiview(data):
    request_data = requests.request(method='post',url=local_url+'token/',data=data)
    return request_data.json()
def get_single_post(request,pk):
    get_all_cat_data = get_all_cat()
    catgeries ={url:url.replace(' ','-') for url in get_all_cat_data}
    data = requests.request(url=local_url + f'api/v1/post/{pk}/', method='get',headers=headers)
    if data.status_code == 401:
        headers['Authorization'] = 'Bearer ' + loginapiview({'username': 'mohan', 'password': '1234'})['access']
        data = requests.request(url=local_url + f'api/v1/post/{pk}/', method='get',headers=headers)
    json_data = data.json()
    title= str(json_data['post_title']+'.txt')
    story_read_data = open(rf"C:\Users\mk302\Downloads\content_creater\all_stories\{title}",'r',encoding='utf-8')
    read_data = story_read_data.read()
    story_read_data.close()
    print(catgeries)
    return render(request, 'individual_post.html', {'post': json_data,'read_story':read_data,'categories':catgeries})
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




def select_category_data(request,cat_name):
    data = CreatePost.objects.all()
    catgeries = get_all_cat()
    catgeries ={url:url.replace(' ','-') for url in catgeries}
    if cat_name:
        select_cat = get_all_cat(cat_name)
        read_file = open(r"new_api\existed_stories.json",'r',encoding='utf-8')
        read_data = json.loads(read_file.read())
        read_file.close()
        select_title = []
        for each_story in read_data:
            for link in  select_cat :
                if link in each_story:
                    select_title.append(each_story[link])
        data = CreatePost.objects.filter(post_title__in = select_title)
        print(data)
    for i in data:
        i.post_id = str(i.post_id).replace('-','')
    like_json_file = 'media/likes_json_data.json'
    file_data = open(like_json_file,'r')
    read_data= file_data.read()
    json_data = json.loads(read_data)
    for i in data:
        i.description = i.description[:10]
        if json_data.get(str(i.post_id),None):
            i.likes = json_data[str(i.post_id)]
    return TemplateResponse(request,'feed.html',{'posts':data})
