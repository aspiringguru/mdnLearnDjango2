from django.shortcuts import render

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_books_titles_contains_red = Book.objects.filter(title__contains='red').count()
    num_books_titles_contains_yellow = Book.objects.filter(title__contains='yellow').count()

    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()


    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    # maintenance books (status = 'm')
    num_instances_maintenance = BookInstance.objects.filter(status__exact='m').count()
    # on_loan books (status = 'o')
    num_instances_on_loan = BookInstance.objects.filter(status__exact='o').count()
    # Reserved books (status = 'r')
    num_instances_reserved = BookInstance.objects.filter(status__exact='r').count()
    #nb class BookInstance has variable status, so variable-name__exact
    # other bookInstance variables

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_genres': num_genres,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_instances_maintenance': num_instances_maintenance,
        'num_instances_on_loan': num_instances_on_loan,
        'num_instances_reserved': num_instances_reserved,
        'num_books_titles_contains_red': num_books_titles_contains_red,
        'num_books_titles_contains_yellow': num_books_titles_contains_yellow,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
