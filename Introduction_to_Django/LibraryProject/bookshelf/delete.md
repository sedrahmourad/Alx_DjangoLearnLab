
---

# Delete Operation

```python
# Open Django shell with: python manage.py shell

from bookshelf.models import Book

# Retrieve the book we want to delete
book = Book.objects.get(title="1984")

# Delete the book
book.delete()
