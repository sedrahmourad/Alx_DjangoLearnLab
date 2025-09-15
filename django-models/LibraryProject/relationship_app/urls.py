from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import list_books
from .views import LibraryDetailView



urlpatterns = [
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register_view, name="register"),
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
    path('add_book/', views.add_book, name='add_book'),                  # changed here
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'), # changed here
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('books/', list_books, name='list_books'),  # function-based view
    path('books/<int:pk>/', LibraryDetailView.as_view(), name='book_detail'), 
]
