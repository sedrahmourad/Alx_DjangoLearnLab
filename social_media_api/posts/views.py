from django.shortcuts import render

# Create your views here.
# posts/views.py

from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# --- Post ViewSet ---
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # NEW: Add search and ordering capabilities
    # We use the global DEFAULT_FILTER_BACKENDS set in settings.py
    
    # Fields to search when '?search=' parameter is used
    search_fields = ['title', 'content', 'author__username'] 
    
    # Fields that can be used for ordering (e.g., ?ordering=-created_at)
    ordering_fields = ['created_at', 'updated_at', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# --- Comment ViewSet ---
class CommentViewSet(viewsets.ModelViewSet):
    # Set of comments the view works with
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Note: We ensure users can only comment on an existing post, but the
    # model serializer handles the Post ForeignKey field from the incoming data.

    # Override the perform_create method to automatically set the author
    def perform_create(self, serializer):
        # Set the author to the logged-in user
        serializer.save(author=self.request.user)
