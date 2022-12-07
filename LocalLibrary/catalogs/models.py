from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import uuid

from django.utils.datetime_safe import date


# Create your models here.
class Genre(models.Model):
    """
       Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=100, help_text='Enter a book genre (e.g. Science Fiction, French Poetry etc.')

    def __str__(self):
        """
               String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Book(models.Model):
    """
        Model representing a book (but not a specific copy of a book).
    """

    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=2000, help_text='Enter a brief description of the book')
    isbn = models.CharField(
        'ISBN',
        max_length=100,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='select a genre for this book')
    lan = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        represent book object
        """
        return self.title

    def get_absolute_url(self):
        """
        returns url access a particular book instance.
        """

        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ''.join([genre.name for genre in self.genre.all()])

    display_genre.short_description = 'GENRE'


class Language(models.Model):
    CHOICE_LAN = [
        ('EN', 'English'),
        ('CN', 'Chinese'),
    ]
    language = models.CharField(choices=CHOICE_LAN, default='EN', blank=True, max_length=20)

    def __str__(self):
        return self.language


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(blank=True, null=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, default='m', blank=True, choices=LOAN_STATUS, help_text='book availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
