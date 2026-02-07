from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode

from .models import User, Post

class PostForm(forms.ModelForm):
    post_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
        'content': forms.Textarea(attrs={
            'placeolder': "What's on your mind?",
            'style':"width: 100%; height: 150px;",
            'autofocus':True
            })
        }
        labels = {
        'content':''
        }

# Custom utility functions, not views
def redirect_with_query(viewname, query_params=None, **kwargs):
    base = reverse(viewname, kwargs=kwargs)
    if query_params:
        return redirect(f"{base}?{urlencode(query_params)}")
    return redirect(base)

def formfiller(_form, **initial):
    return _form(initial=initial)

# Views
@login_required
def index(request):
    section = request.GET.get('section')
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    name = request.user.username
    follow = ''
    following = ''
    followers = ''
    try:
        posts = Post.objects.all().order_by('-created_at')
        if section == 'following':
            p = Paginator(posts.filter(writer__in=request.user.following.all()), 10)

        elif section == 'profile':
            name = request.GET.get('name')
            p = Paginator(posts.filter(writer__username=name), 10)
            user = get_object_or_404(User, username=name)
            following = user.following_count
            followers = user.follower_count
            if name != request.user.username:
                if user in request.user.following.all():
                    follow = 'UnFollow'
                else:
                    follow = 'Follow'
            
        elif section == 'posts':
            section = 'posts'
            p = Paginator(posts, 10)

        else:
            return render(request, f'network/index.html')
        p = p.get_page(page)
        data = {
        'posts': p,
        'next': p.has_next(),
        'prev': p.has_previous(),
        'following': following,
        'followers': followers,
        'follow': follow,
        'name': name,
        }
        data = {'html':render_to_string(f"network/partials/{section}.html", data, request=request)} | {'next':data['next'], 'prev':data['prev']}
        return JsonResponse(data)
    except EmptyPage:
        return redirect_with_query('index', {'section':section, 'page':1}, request=request)

@login_required
def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest("Invalid Data")
        content = form.cleaned_data['content']
        id = form.cleaned_data['post_id']
        if not content:
            return HttpResponseBadRequest('Cannot make a new post with no content')
        if id:
            try:
                post = Post.objects.get(pk=id, writer=request.user)
            except Post.DoesNotExist:
                return HttpResponseBadRequest("You donot have permissions to edit this post.")
            post.content = content
            post.save()
        else:
            Post.objects.create(writer=request.user, content=content)
        return redirect('index')

    elif request.method == 'GET':
        id = request.GET.get('post_id', '')
        try:
            post = Post.objects.get(writer=request.user, id=id)
        except:
            post = None
        form = PostForm(initial={'content':'' if post is None else post.content, 'post_id':'' if post is None else post.id})
        return render(request, "network/posts.html", {'post_form':form})

    return HttpResponseBadRequest("Only GET or POST Allowed")

@login_required
def like(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Post Required")
    
    id = int(request.POST.get('id'))
    post = get_object_or_404(Post, id=id)
    if request.user.id == post.writer.id:
        return HttpResponseBadRequest("Cannot Like your own post")
        
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({'success':True, 'action':'like', 'like_class':'btn btn-primary' if liked else 'btn btn-danger', 'likes':post.like_count})

@login_required
def follow(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Post Required")
    
    whom = request.POST.get('whom')
    user = get_object_or_404(User, username=whom)

    if user.id == request.user.id:
        return HttpResponseBadRequest("Cannot Follow Yourself")

    if user in request.user.following.all():
        request.user.following.remove(user)
        followed = False
    else:
        request.user.following.add(user)
        followed = True

    return JsonResponse({'success':True, 'action':'follow', 'follow':'UnFollow' if followed else 'Follow', 'following':user.following_count, 'followers':user.follower_count})

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
