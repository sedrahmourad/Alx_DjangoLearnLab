from django.shortcuts import render
from .models import Post

# Create your views here.

def home(request):
    return render(request, "blog/index.html")

def post_list(request):
    posts = Post.objects.all()
    return render(request, "blog/posts.html", {"posts": posts})
