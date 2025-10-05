from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Profile, Comment, Post, Tag
from taggit.forms import TagWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_picture"]
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={"rows":3, "placeholder": "Write your comment..."}),
        max_length=2000,
        label=""
    )
    class Meta:
        model = Comment
        fields = ["content"]
    def clean_content(self):
        data = self.cleaned_data["content"]
        if not data.strip():
            raise forms.ValidationError("comment cannot be empty")
        return data

class PostForm(forms.ModelForm):
    # tags input as a comma-separated string
    tags_field = forms.CharField(
        required=False,
        label="Tags (comma separated)",
        widget=forms.TextInput(attrs={"placeholder": "e.g. django, tutorials, tips"})
    )

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets = {
            "tags": TagWidget(attrs={"placeholder": "Add tags separated by commas"})
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance", None)
        super().__init__(*args, **kwargs)
        # If editing a Post, pre-fill tags_field from existing tags
        if instance:
            self.fields["tags_field"].initial = ", ".join([t.name for t in instance.tags.all()])

    def clean_tags_field(self):
        data = self.cleaned_data.get("tags_field", "")
        # normalize: split by comma, strip whitespace, remove empties, unique
        tags = [t.strip() for t in data.split(",") if t.strip()]
        # optional: lower-case or other normalization
        return list(dict.fromkeys(tags))

    def save(self, commit=True):
        # Save Post instance first, then handle Tag M2M
        post = super().save(commit=False)
        if commit:
            post.save()
        # handle tags
        tags_list = self.cleaned_data.get("tags_field", [])
        # clear existing tags then add
        post.tags.clear()
        for tag_name in tags_list:
            tag_obj, created = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag_obj)
        if commit:
            post.save()
        return post