from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class Book(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateField('year published')
    authors = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)
    description = models.TextField(max_length=2000)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.pub_date.year})"
    
class CustomerLoan(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateField('loan date', default=timezone.now)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    due_back = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} ({self.due_back})"

class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(CustomerLoan, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    image = models.ImageField(upload_to='cover/')