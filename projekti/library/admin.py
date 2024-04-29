from django.contrib import admin
from .models import Book, Author, Genre, CustomerLoan

class BookAdmin(admin.ModelAdmin):
    list_display = ('cover', 'title', 'get_authors_last_names', 'description', 'pub_date', 'is_available', 'borrower_username')
    search_fields = ['title', 'genres__name', 'pub_date', 'authors__last_name', 'customerloan__customer__username']
    list_filter = ['pub_date', 'authors', 'genres', 'is_available']
    list_editable = ['is_available']  # Fields editable in the list view
    list_display_links = ('title',)  # Make the title field clickable

    def get_authors_last_names(self, obj):
        return ", ".join([author.last_name for author in obj.authors.all()])
    get_authors_last_names.short_description = 'Authors'

    def borrower_username(self, obj):
        loan = obj.customerloan_set.first()  # Get the first loan associated with the book
        if loan:
            return loan.customer.username
        return None
    borrower_username.short_description = 'Borrower'

    def save_model(self, request, obj, form, change):
        if obj.is_available:
            # If the book is marked as available, remove any associated loans
            obj.customerloan_set.all().delete()
        super().save_model(request, obj, form, change)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    search_fields = ['first_name', 'last_name']

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
