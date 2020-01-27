from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


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

    # Number of visits to this view, as counted in the session variable.
    # https://docs.djangoproject.com/en/2.2/topics/http/sessions/
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_genres': num_genres,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'num_instances_maintenance': num_instances_maintenance,
        'num_instances_on_loan': num_instances_on_loan,
        'num_instances_reserved': num_instances_reserved,
        'num_books_titles_contains_red': num_books_titles_contains_red,
        'num_books_titles_contains_yellow': num_books_titles_contains_yellow,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    #paginate_by = 10
    paginate_by = 2
    #context_object_name = 'my_book_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='red')[:5] # Get 5 books containing the title war
    #template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    template_name = 'book_list.html'  # Specify your own template name/location

    def get_queryset(self):
        return Book.objects.filter(title__icontains='yellow')[:5] # Get 5 books containing the title war

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(generic.DetailView):
    model = Book
    '''
    def book_detail_view(request, primary_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')
        return render(request, 'catalog/book_detail.html', context={'book': book})
    '''
    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book': book})


class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
        Generic class-based view listing books on loan to current user.
        nb: status__exact='o'
        nbb: replicate this to make overdue by user class.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
