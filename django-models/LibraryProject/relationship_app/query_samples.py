# relationship_app/query_samples.py
# Usage: python manage.py shell < relationship_app/query_samples.py
# (Or run inside a Django shell interactively.)

from relationship_app.models import Author, Book, Library, Librarian

# --- Sample data creation (safe: uses get_or_create) ---
author, _ = Author.objects.get_or_create(name="George Orwell")
book1, _ = Book.objects.get_or_create(title="1984", author=author)
book2, _ = Book.objects.get_or_create(title="Animal Farm", author=author)

library, _ = Library.objects.get_or_create(name="Central Library")
# add books to library if not already added
library.books.add(book1, book2)

librarian, created = Librarian.objects.get_or_create(name="Alice", library=library)

# --- Query 1: Query all books by a specific author ---
print("Query 1: Books by George Orwell (using Author.books):")
books_by_author = author.books.all()   # thanks to related_name='books'
print([b.title for b in books_by_author])

# Alternate: Using Book.objects.filter
books_by_author2 = Book.objects.filter(author__name="George Orwell")
print("Query 1 (alt):", [b.title for b in books_by_author2])

# --- Query 2: List all books in a library ---
print(f"\nQuery 2: Books in library '{library.name}':")
books_in_library = library.books.all()
print([b.title for b in books_in_library])

# --- Query 3: Retrieve the librarian for a library ---
print(f"\nQuery 3: Librarian for library '{library.name}':")
print(library.librarian.name)  # thanks to related_name='librarian'
