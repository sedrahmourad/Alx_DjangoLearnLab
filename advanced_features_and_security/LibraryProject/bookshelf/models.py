from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_edit", "can edit book"),
            ("can_view", "can view book"),
            ("can_create", "can create book"),
            ("can_delete", "can delete book"),
        ]

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

# custom user manager 
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
       
        if not username:
            raise ValueError("The Username field is required")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # hashes password
        user.save(using=self._db)
        return user 
# create super user   
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a superuser (admin).
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

# create a custom user model 
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(blank=True, null= True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    objects = CustomUserManager()
    
    def __str__(self):
        return self.username  
