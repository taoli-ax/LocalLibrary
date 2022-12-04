from django.http import HttpResponse
from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views import generic


# Create your views here.
def index(request):
    book_num = Book.objects.count()
    num_instances = BookInstance.objects.count()
    authors = Author.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_genre = Genre.objects.count()
    num_power_book = Book.objects.filter(title__icontains='Power').count()
    nums_visit = request.session.get('nums_visit', 0)
    request.session['nums_visit'] = nums_visit + 1
    context = {
        'num_books': book_num,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': authors,
        'num_genre': num_genre,
        'num_power_book': num_power_book,
        'nums_visit': nums_visit,
    }
    return render(request, 'index.html', context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all()
    template_name = 'book_list.html'


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    queryset = Author.objects.all()
    template_name = 'author_list.html'


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'
