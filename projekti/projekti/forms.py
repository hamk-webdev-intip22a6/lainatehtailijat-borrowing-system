from django import forms
from .models import Book

class UploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['cover']