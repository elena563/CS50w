from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"page_obj": page_obj })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def post(request):
    if request.method == "GET":
        return render(request, "network/post.html")
    else:
        print("POST endpoint hit!")
        data = json.loads(request.body)
    
        image = data.get("image", "")
        content = data.get("content", "")

        post = Post(
            poster=request.user,
            image=image,
            content=content,
        )
        post.save()

        return JsonResponse({"message": "Post created successfully."}, status=201)
    
@csrf_exempt
@login_required
def like_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user) 
    else:
        post.likes.add(user)    
    return JsonResponse({'likes': post.likes.count()})

def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(poster=user).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    followers_count = user.followers.count()
    following_count = user.following.count()
    is_following = False
    if request.user.is_authenticated:
        is_following = request.user in user.followers.all()
    return render(request, "network/profile.html", {
        "profile_user": user,
        "page_obj": page_obj,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following
    })

@login_required
def following(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(poster__in=user.following.all()).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {"page_obj": page_obj, "profile_user": user})

@login_required
def follow(request, username):
    user_to_follow = User.objects.get(username=username)
    current_user = request.user
    if current_user in user_to_follow.followers.all():
        current_user.following.remove(user_to_follow)
    else:
        current_user.following.add(user_to_follow)
    return HttpResponseRedirect(reverse("profile", args=[username]))

@csrf_exempt
@login_required
def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user != post.poster:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    if request.method == 'POST':
        data = json.loads(request.body)
        post.content = data.get('content', post.content)
        post.save()
        return JsonResponse({'content': post.content})