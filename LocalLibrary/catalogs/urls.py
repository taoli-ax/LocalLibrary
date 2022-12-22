from django.contrib import admin
from django.urls import path, include
from django.urls import path
from .views import (
    index,
    BookListView,
    BookDetailView,
    AuthorListView,
    AuthorDetailView,
    LoanedBookByUserListView,
    AllLoanedBookForAdminListView,
)

urlpatterns = [
    path('', index, name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('mybooks/', LoanedBookByUserListView.as_view(), name='my-borrowed'),
    path('allbooks/',AllLoanedBookForAdminListView.as_view(), name='all-borrowed'),
]
