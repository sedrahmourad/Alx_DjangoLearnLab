from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book

# Create your views here.


@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    """Only users with can_view permission can see this list."""
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'book_list': books})


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

