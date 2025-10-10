from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    # Endpoint for new user creation
    path('register/', RegisterView.as_view(), name='register'), 
    
    # Endpoint for existing user login and token retrieval
    path('login/', LoginView.as_view(), name='login'),
]