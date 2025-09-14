
---

## 📘 `update.md`
```markdown
# Update Operation

```python
from book_store.models import Book

# Get the book we created
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Confirm the update
book.title
# Expected Output: 'Nineteen Eighty-Four'
