from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book

# Customizing how Book is displayed in the admin
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # show these columns
    list_filter = ('publication_year', 'author')  # sidebar filters
    search_fields = ('title', 'author')  # search box

# Register the Book model with the custom admin settings
admin.site.register(Book, BookAdmin)

