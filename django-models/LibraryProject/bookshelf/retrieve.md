# Retrieve Operation

```python
# Open Django shell with: python manage.py shell

from bookshelf.models import Book

# Retrieve the book we created
book = Book.objects.get(title="1984")

# Display its attributes
print(book.title)   # Expected: 1984
print(book.author)  # Expected: George Orwell
print(book.publication_year)  # Expected: 1949
