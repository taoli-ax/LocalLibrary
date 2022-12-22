import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView

from .models import Book, BookInstance, Author, Genre
from django.views import generic
from .forms import RenewBookForm


# Create your views here.
@login_required
def index(request):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
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


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all()
    template_name = 'book_list.html'


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    queryset = Author.objects.all()
    template_name = 'author_list.html'


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = 'author_detail.html'


class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'

    def get_queryset(self):
        return BookInstance.objects. \
            filter(borrower=self.request.user). \
            filter(status__exact='o'). \
            order_by('due_back')


class AllLoanedBookForAdminListView(generic.ListView, PermissionRequiredMixin, LoginRequiredMixin):
    model = BookInstance
    permission_required = 'catalogs.can_mark_as_returned'
    template_name = 'all_borrowed_book_for_admin.html'

    def get_queryset(self):
        return BookInstance.objects.all().order_by('due_back')


def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')