from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from network.models import User, Post, Follow, Like

def index(request):
   #pagination
    posts = Post.objects.all().order_by('-timestamp') # order by the latest posts
    return render(request, "network/index.html", {
        "page_obj": pagination(request, posts),
        'check_like': check_like(request)
    })


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



#add a new post
def new_post(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        post = Post.objects.create(user = request.user, post_content = data.get('post_content'))
        return JsonResponse({
            'id': post.id,
            "username": post.user.username,
            "user_id": post.user.id,
            "post_content": post.post_content,
            "timestamp": post.timestamp.strftime("%B %d, %Y, %I:%M %p")     
            },status = 200)
    else:
        return HttpResponseRedirect(reverse("login"))


# view users profile
def profile(request, user_id):
    if request.user.is_authenticated: 
        user = User.objects.get(pk = user_id)
        posts = user.posts.all().order_by('-timestamp')  # user posts in reverse chr.order
            
        return render(request, 'network/profile.html', {
            "want_follow": user,
            "field": 'true' if Follow.objects.filter(follower = request.user, following = user).exists() else 'false',
            "followings": Follow.objects.filter(follower = user).count(), # у скольких user в подписчиках лежит=кол.во подписок
            'followers' : Follow.objects.filter(following = user).count(),
            'page_obj': pagination(request, posts),
            "check_like": check_like(request)        
        }, status = 200)
    else:
        return HttpResponseRedirect(reverse("login"))
        

# unfollow and follow buttons
def follow_unfollow(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("message") == 'follow':
            following = User.objects.get(pk = id)
            if not Follow.objects.filter(follower = request.user, following = following).exists():
                Follow.objects.create(follower = request.user, following = following)
                return JsonResponse({
                    'following': Follow.objects.filter(follower = following).count(),
                    "follower": Follow.objects.filter(following = following).count(),
                    "message": "You have been followed successfully"
                }, status=200)
            else:
                return JsonResponse({
                    "error": "You can't follow the same user twice"
                }, status=404)
        else:
            following = User.objects.get(pk = id)
            if Follow.objects.filter(follower = request.user, following = following).exists():
                field = Follow.objects.get(follower = request.user, following = following)
                field.delete()
                return JsonResponse({
                    'following': Follow.objects.filter(follower = following).count(),
                    "follower": Follow.objects.filter(following = following).count(),
                        "message": "You have unfollowed successfully"
                    }, status=200)
            else:
                return JsonResponse({
                    "error": "You can't unfollow the user if you haven't followed them"
                }, status=404)
                

            
    return HttpResponseRedirect(reverse("profile", args = [id]))


def following(request):
    follow = Follow.objects.filter(follower = request.user).values_list('following', flat=True)
    if follow:
        users = User.objects.filter(id__in= follow)
        all_posts = []
        for user in users:
            all_posts.extend(user.posts.all())
        page_obj = pagination(request, all_posts)
        following = True # user has followings
    else:
        following = False
        page_obj = ''   #page is empty because user does not have any following
        
    return render(request, "network/following.html", {
        'page_obj': page_obj,
        'check_follow': following,
        "check_like": check_like(request)
    })
    

#pagination
def pagination(request, posts):
    paginator = Paginator(posts, 10) # 10 posts on each page
    
    # if request has no page, page number=1 because user hasn't pressed any button
    if request.GET.get('page')!='' and request.GET.get('page')!=None: 
        page_number = int(request.GET.get('page'))
    else:
        page_number = 1
        
    return paginator.get_page(page_number) # all posts on that page
    
    
#create a function for post edits
def edit_posts(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get('message') is not None and data.get('post_id') is not None:
            post_id = data.get('post_id')
            message = data.get('message')
            post = Post.objects.get(pk = post_id)
            if message == "like":
                # if user has already liked True else False(hearts)
                if not Like.objects.filter(post = post, user = request.user).exists(): # if field exists user has liked the post
                    Like.objects.create(post = post, user = request.user)
                    return JsonResponse({
                        "likes": post.likepost.count()
                    }, status = 200)
                else:
                    return JsonResponse({
                        "error": "You can't like the post twice"
                    }, status = 404)
            else:
                if Like.objects.filter(post = post, user = request.user).exists():
                    like = Like.objects.get(post = post, user = request.user)
                    like.delete()
                    return JsonResponse({
                        "likes": post.likepost.count()
                    }, status = 200)
                else:
                    return JsonResponse({
                        "error": "You can't dislike the post if you haven't liked it"
                    }, status = 404)
        
                    
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get('new_content') is not None and data.get('edit_post_id') is not None:
            id = data.get('edit_post_id')    
            edit = Post.objects.get(id = id)
            if request.user == edit.user:
                edit.post_content = data.get('new_content')
                edit.save()
                return JsonResponse({
                    'edited': edit.post_content
                }, status = 200)
            else:
                return JsonResponse({
                    "error": "Permission denied. Not the author of the post"}, status = 403)
 
 
# if user has already liked the post
def check_like(request):
    if request.user.is_authenticated:
        user = Like.objects.filter(user = request.user)
        return [i.post for i in user]
    return None
 
 
 

           