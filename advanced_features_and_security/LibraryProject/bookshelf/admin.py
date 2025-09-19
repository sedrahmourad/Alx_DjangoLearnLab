from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

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
# custom user admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields to be displayed in the user list in admin panel
    list_display = ("username", "email", "date_of_birth", "is_staff", "is_active")

    # Fields available for filtering in the admin panel
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    # Fields layout when viewing/editing a user
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields layout when adding a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "date_of_birth", "profile_photo", "password1", "password2", "is_staff", "is_active")}
        ),
    )

    search_fields = ("username", "email")
    ordering = ("username",)


#  Register the custom user model with custom admin
admin.site.register(CustomUser, CustomUserAdmin)
