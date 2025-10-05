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

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        # Attach the logged-in user as the comment author
        form.instance.author = self.request.user
        # Attach the comment to the correct post
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the blog post detail page after commenting
        return reverse('post_detail', kwargs={'pk': self.kwargs['post_id']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.id})

    def test_func(self):
        # Only the comment author can edit
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.id})

    def test_func(self):
        # Only the comment author can delete
        comment = self.get_object()
        return self.request.user == comment.author