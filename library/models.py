from django.db import models
from datetime import date, timedelta

from Accounts.models import Account

# Create your models here.
categories_choices =(
    ('Romance','Romance'),
    ('Science Fiction','Science Fiction'),
    ('Biographies','Biographies'),
    ('Self-Help','Self-Help'),
)
class Book(models.Model):
    name = models.CharField(max_length=200)
    isbn = models.PositiveBigIntegerField(unique=True)
    author = models.CharField(max_length=90)
    quantity = models.PositiveIntegerField(default=1)
    categories = models.CharField(max_length=100, choices=categories_choices)

    def __str__(self):
        return str(self.name)
    
class IssueRequest(models.Model):
    student = models.ForeignKey(Account, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_issued = models.BooleanField(default=False)
    issued_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.book.name


def expiry():
    return date.today() + timedelta(days=30)

class IssuedBooks(models.Model):
    issuerequest = models.ForeignKey(IssueRequest, on_delete=models.CASCADE)
    issuedby = models.ForeignKey(Account, on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)

