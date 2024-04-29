from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('browse/', views.browse, name='browse'),
    path('search/', views.search, name='search'),
    path('loan/<int:book_id>/', views.loan_book, name='loan_book'),  # URL for borrowing a book
    path('return/<int:loan_id>/', views.return_book, name='return_book'),  # URL for returning a book
    path('my-loans/', views.my_loans, name='my_loans'),  # URL for my_loans page
]
