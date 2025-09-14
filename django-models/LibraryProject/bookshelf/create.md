# Create Operation

```python
# Open Django shell with: python manage.py shell

from bookshelf.models import Book

# Create a Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Check what was created
print(book)
