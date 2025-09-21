import json
import math
import os
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.core.paginator import Paginator
from rest_framework.response import Response
from .forms import Createpostform, CreateCommentform
from curd.models import CreatePost, User
from new_api.constan_data import page_size

local_url = 'http://127.0.0.1:8000/'

# ✅ Use environment variables / settings for base URLs
API_BASE_URL = getattr(settings, "API_BASE_URL", local_url)
LOCAL_STORIES_PATH = os.path.join(settings.MEDIA_ROOT, "stories")
LIKE_JSON_FILE = os.path.join(settings.MEDIA_ROOT, "likes_json_data.json")

headers = {"Authorization": ""}


def get_all_cat(cat_name=None):
    """Fetch categories from API"""
    response = requests.get(f"{API_BASE_URL}api/v1/categories/")
    response.raise_for_status()
    cat_data = response.json()
    data = {url: url.replace(" ", "-") for url in cat_data}
    return data


def home(request):
    return TemplateResponse(request, "home.html", {"catgeries": get_all_cat()})


def create_post(request):
    """Handle create post with file upload via API"""
    form_data = Createpostform(request.POST or None, request.FILES or None)
    headers["Authorization"] = "Bearer " + loginapiview({"username": "mohan", "password": "1234"})["access"]
    if request.method == "POST" and form_data.is_valid():
        request_data = form_data.cleaned_data

        files = {}
        if "image" in request.FILES:
            files["image"] = request.FILES["image"]

        # Remove unwanted fields
        request_data.pop("csrfmiddlewaretoken", None)
        request_data.pop("image", None)

        api_data = requests.post(
            url=f"{API_BASE_URL}api/v1/create_post/",
            headers=headers,
            data=request_data,
            files=files
        )
        api_response = api_data.json()
        return redirect(f"/view_single_post/{api_response['post_id']}")

    return TemplateResponse(request, "create_post.html", {"data": form_data, "catgeries": get_all_cat()})


def feed(request):
    """Feed page with pagination + category filtering"""
    page_num = request.GET.get("page")
    category = request.GET.get("category")
    author = request.GET.get("author")
    page_num_url = f"?page={page_num}" if page_num else ""
    category_url = f"category={category}" if category else ""
    category_url = "&"+category_url if page_num_url else "?"+category_url
    author_url = f"author={author}" if author else ""
    author_url = "&" + author_url if page_num_url else "?" + author_url
    params = []
    if page_num:
        params.append(f"page={page_num}")
    if category:
        params.append(f"category={category}")
    if author:
        params.append(f"author={author}")
    query_string = "?" + "&".join(params) if params else ""

    request_url = f"{API_BASE_URL}api/v1/get_data/{query_string}"
    api_data = requests.get(request_url)
    data = api_data.json()
    last_page = math.ceil(data["count"] / page_size)
    current = int(page_num) if page_num else 1
    previous = current - 1 if data["previous"] else None
    next_page = current + 1 if data["next"] else None

    feed_data = data["results"]
    # Load likes from JSON file
    if os.path.exists(LIKE_JSON_FILE):
        with open(LIKE_JSON_FILE, "r", encoding="utf-8") as file:
            likes_data = json.load(file)
    else:
        likes_data = {}

    for post in feed_data:
        # post["post_id"] = str(post["post_id"]).replace("-", "")
        if likes_data.get(post["post_id"]):
            post["likes"] = likes_data[post["post_id"]]
    print(feed_data)
    return TemplateResponse(
        request,
        "feed.html",
        {
            "posts": feed_data,
            "catgeries": get_all_cat(),
            "current": current,
            "next": next_page,
            "previous": previous,
            "last_page": last_page,
            "category": category,
            "author":author
        },
    )

def get_data_tags(request , pk,tag_name):
    data = requests.request(url=API_BASE_URL+ f'api/v1/tags/{pk}/{tag_name}', method='get')
    if data.status_code==401:
        headers['Authorization'] = 'Bearer ' + loginapiview({'username': 'mohan', 'password': '1234'})['access']
        data = requests.request(url=API_BASE_URL + f'api/v1/tags/{pk}/{tag_name}', method='get')
    return redirect('/show_feed/')

def delete_post(request, pk):
    requests.delete(f"{API_BASE_URL}api/v1/delete_post/{pk}/", headers=headers)
    return redirect("/feed/")


def loginapiview(data):
    response = requests.post(f"{API_BASE_URL}token/", data=data)
    return response.json()


def get_single_post(request, pk):
    """Show single post with content from txt file"""
    response = requests.get(f"{API_BASE_URL}api/v1/post/{pk}/", headers=headers)
    if response.status_code == 401:
        headers["Authorization"] = "Bearer " + loginapiview({"username": "mohan", "password": "1234"})["access"]
        response = requests.get(f"{API_BASE_URL}api/v1/post/{pk}/", headers=headers)
    json_data = response.json()
    post_id = json_data["post_id"]
    story_path = os.path.join(LOCAL_STORIES_PATH, f"{post_id}.txt")

    with open(story_path, "r", encoding="utf-8") as f:
        read_data = f.read()

    return render(
        request,
        "individual_post.html",
        {"post": json_data, "read_story": read_data, "catgeries": get_all_cat()},
    )


def createcomment(request,pk):
    if request.method=='POST':
        payload = {}
        comment_desc = request.POST['description']
        payload['description'] = comment_desc
        payload['Image url'] = None
        headers = {'Content-Type':'application/json'}
        data = requests.post(f"{API_BASE_URL}api/v1/create_comment/{pk}",json = payload, headers=headers)
    return redirect(f'/view_single_post/{pk}')

def search_data(request):
    all_cat = get_all_cat()
    text = request.GET.get('q')
    print(request.path)
    for i in all_cat.keys():
        if text.strip().lower() in i:
            return redirect(f"feed/?category={i}")
    else:
        return redirect(request.path)