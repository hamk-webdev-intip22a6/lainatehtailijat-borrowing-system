from django.shortcuts import render, redirect
from .models import Book, CustomerLoan
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q

def browse(request):
    all_books = Book.objects.all()
    return render(request, 'library/browse.html', {'all_books': all_books})

def search(request):
    query = request.GET.get('query')
    if query:
        # Perform case-insensitive search for books with title containing the query
        title_results = Book.objects.filter(title__icontains=query)
        # Perform case-insensitive search for books with authors containing the query
        author_results = Book.objects.filter(authors__first_name__icontains=query) | \
                         Book.objects.filter(authors__last_name__icontains=query)
        # Perform case-insensitive search for books with genres containing the query
        genre_results = Book.objects.filter(genres__name__icontains=query)
        # Combine title, author, and genre results
        books = (title_results | author_results | genre_results).distinct()
    else:
        books = []
    return render(request, 'library/search_results.html', {'books': books, 'query': query})

@login_required
def loan_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book.is_available:
        # Calculate due date (30 days from today)
        due_date = timezone.now() + timedelta(days=30)
        # Create a new loan entry associated with the current user
        loan = CustomerLoan(customer=request.user, book=book, due_back=due_date)
        loan.save()
        # Update the availability status of the book
        book.is_available = False
        book.save()
    return redirect('library:browse')

def return_book(request, loan_id):
    # Retrieve the loan object based on the provided loan_id
    loan = CustomerLoan.objects.get(pk=loan_id)
    # Retrieve the corresponding book object
    book = loan.book
    # Delete the loan entry
    loan.delete()
    # Update the availability status of the book to indicate it's available again
    book.is_available = True
    book.save()
    # Redirect the user back to the browsing page
    return redirect('library:my_loans')  # Redirect to the 'my_loans' page

@login_required
def my_loans(request):
    if request.user.is_authenticated:
        # Query loans currently on loan for the logged-in user
        user_loans = CustomerLoan.objects.filter(customer=request.user)
        return render(request, 'library/my_loans.html', {'user_loans': user_loans})
    else:
        return render(request, 'library/my_loans.html')

