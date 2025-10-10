from rest_framework import serializers
from .models import Post, Comments
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'post', 'author', 'created_at', 'content', 'author_username']
        read_only_fields = ['author', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    comment_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'title', 'content', 
                  'created_at', 'updated_at', 'comments', 'comment_count']
        read_only_fields = ['author', 'created_at', 'updated_at', 'comment_count']
    def get_comment_count(self, obj):
        return obj.comments.count()