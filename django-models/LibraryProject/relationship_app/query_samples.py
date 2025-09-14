import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
author_name = "George Orwell"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)
print(f"Books by {author_name}:")
for book in books_by_author:
    print(f"- {book.title}")

# 2. List all books in a library
library_name = "Central Library"
library = Library.objects.get(name=library_name)   # ✅ Required line
books_in_library = library.books.all()
print(f"\nBooks in {library_name}:")
for book in books_in_library:
    print(f"- {book.title}")

# 3. Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print(f"\nThe librarian for {library_name} is {librarian.name}.")

