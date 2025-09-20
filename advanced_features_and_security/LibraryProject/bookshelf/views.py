from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book
from django.db import connection 
from .forms import BookSearchForm


# Create your views here.


@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    """
    Only users with can_view permission can see this list.
    Optionally allows searching books by title/author safely.
    """
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():  # input is validated
        q = form.cleaned_data.get("q")
        if q:
            books = books.filter(title__icontains=q) | books.filter(author__icontains=q)

    return render(request, 'books/book_list.html', {
        'book_list': books,
        'form': form
    })


@permission_required('relationship_app.can_create', raise_exception=True)
def create_book(request):
    """Only Editors and Admins can create books."""
    if request.method == "POST":
        # (simplified example)
        title = request.POST.get('title')
        author = request.POST.get('author')
        year = request.POST.get('publication_year')
        Book.objects.create(title=title, author=author, publication_year=year)
        return HttpResponse("Book created!")
    return render(request, 'books/create_book.html')


@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    """Only Editors and Admins can edit books."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.title = request.POST.get('title', book.title)
        book.save()
        return HttpResponse("Book updated!")
    return render(request, 'books/edit_book.html', {'book': book})


@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    """Only Admins can delete books."""
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return HttpResponse("Book deleted!")

# Example of avoiding raw SQL. If you absolutely must use raw(), use paramization:
def dangerous_example_need_raw(request):
    # BAD: never format user input into SQL
    # safe way:
    user_q = request.GET.get("q", "")
    if user_q:
        # Use ORM or parameterized raw query
        qs = Book.objects.raw("SELECT * FROM bookshelf_book WHERE title LIKE %s", [f"%{user_q}%"])
    else:
        qs = Book.objects.none()
    return render(request, "bookshelf/book_list.html", {"books": qs})
