from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='posts'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    # Post detail (already exists)
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),

    # Comment URLs
   path('posts/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]
]
