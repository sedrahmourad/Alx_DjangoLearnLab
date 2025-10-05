from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm,
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from .models import Post, Comment
from .forms import CommentForm
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

@login_required
def add_comment(request, post_id):
    """Add a new comment to a post"""
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Your comment was posted.")
            return redirect("post_detail", pk=post.id)
    else:
        form = CommentForm()
    return render(request, "blog/comment_form.html", {"form": form})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit a comment (only by the author)"""
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a comment (only by the author)"""
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        messages.success(self.request, "Comment deleted.")
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})