from django.contrib import admin
from .models import Book, Language, Author, BookInstance, Genre

# Register your models here.
# admin.site.register(Book)
admin.site.register(Language)
# admin.site.register(Author)
# admin.site.register(BookInstance)
admin.site.register(Genre)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'display_genre', 'lan')
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'status', 'due_back', 'borrower')
    list_filter = ('book', 'status', 'due_back')
    fieldsets = (
        ('info', {'fields': ('book', 'id', 'imprint', 'borrower')}),
        ('availability', {'fields': ('status', 'due_back')})
    )


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

