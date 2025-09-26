from django.urls import path, include  
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register( r'books_all', BookViewSet, basename='book_all' )

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),   # Maps to the BookList view
    # Routes for the BookViewSet (CRUD operations)
    path('', include(router.urls)),
    # ✅ Endpoint to retrieve a token (login)
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
]

