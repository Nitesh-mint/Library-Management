from django import forms

from .models import Book, IssueRequest


class AddBook(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['name','isbn','author', 'categories']

    # def __init__(self, *args, **kwargs):
    #     super(AddBook, self).__init__(*args, **kwargs)
    #     self.fields['name'].widget.attrs['class'] = 'form-control'


class IssueBookForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label="Book Name", to_field_name="name", label="Book Name")