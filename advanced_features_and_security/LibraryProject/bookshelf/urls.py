# bookshelf/urls.py
from django.urls import path
from . import views

app_name = "bookshelf"

urlpatterns = [
    path("", views.book_list, name="book_list"),
    # add other paths such as form submission endpoints
]
