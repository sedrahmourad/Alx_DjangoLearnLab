from django.shortcuts import render, redirect
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm,
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
# Create your views here.

def home(request):
    return render(request, "blog/index.html")

def post_list(request):
    posts = Post.objects.all()
    return render(request, "blog/posts.html", {"posts": posts})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # redirect to login after successful signup
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})
@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")  # avoid re-submitting form on refresh
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "blog/profile.html", context)