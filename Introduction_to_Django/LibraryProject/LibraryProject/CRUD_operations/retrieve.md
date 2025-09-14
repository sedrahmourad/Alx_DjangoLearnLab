
---

## 📘 `retrieve.md`
```markdown
# Retrieve Operation

```python
from book_store.models import Book

# Get the first book from the database
book = Book.objects.first()
book.title
# Expected Output: '1984'

book.author
# Expected Output: 'George Orwell'

book.publication_year
# Expected Output: 1949
