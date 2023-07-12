from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from .models import Book, IssueRequest, IssuedBooks
from .forms import AddBook, IssueBookForm
from Accounts.models import Account

def index(request):
    return render(request, 'index.html')

@user_passes_test(lambda user:not user.is_admin) #this restricts user to access the website
def student_home(request):
    return render(request, 'student/home.html',{'user':request.user})

@user_passes_test(lambda user:user.is_admin)
def admin_home(request):
    return render(request, 'admin/home.html',{'user':request.user})

@user_passes_test(lambda user:user.is_admin)
def add_book(request):
    form = AddBook(request.POST)
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data['name']
            isbn = form.cleaned_data['isbn']
            author = form.cleaned_data['author']
            categories = form.cleaned_data['categories']

            book = Book.objects.create(name=name, isbn=isbn, author=author, categories=categories)
            book.save()
            messages.success(request, "Books addedd successfully!")
        else:
            messages.error(request, "Failed to add books!")
    else:
        form = AddBook()
    return render(request, 'admin/add_book.html', {'form':form})


@user_passes_test(lambda user:not user.is_admin)
def available_books(request):
    books = Book.objects.all()
    return render(request, 'student/books.html',{'books':books,'user':request.user})


@user_passes_test(lambda user: user.is_admin)
def students(request):
    student = Account.objects.filter(is_admin=False)
    return render(request, 'admin/students.html', {'students':student})

@user_passes_test(lambda user:not user.is_admin)
def issueBook(request):
    if request.method == "POST":
        form = IssueBookForm(request.POST)
        if form.is_valid():
            student = request.user
            book_name = form.cleaned_data['book']
            print(book_name)
            book_object = Book.objects.get(name=book_name)
            if IssueRequest.objects.filter(student=student,book=book_object).exists():
                messages.error(request, "You have already requested that book!")
                return redirect("issuebook")
            issue = IssueRequest.objects.create(student=student, book=book_object)
            issue.save()
            messages.success(request, "Book request sent succesfull")
        else:
            messages.error(request, "Failed to send request")
    else:
        form = IssueBookForm()
    return render(request, "student/issuebook.html",{'form':form})


@user_passes_test(lambda user:not user.is_admin)
def issueBook_noform(request, book_id):
    try:
        book_object = Book.objects.get(id=book_id)
        if IssueRequest.objects.filter(student=request.user,book=book_object).exists():
            messages.error(request, "You have already requested that book!")
            return redirect("available_books")
        issue = IssueRequest.objects.create(student=request.user, book=book_object)
        issue.save()
        messages.success(request, "Your Book request has been sent succesfully!")
    except KeyError as e:
        print(e)
    return redirect("available_books")

@user_passes_test(lambda user:user.is_admin)
def issueRequests(request):
    issuerequests = IssueRequest.objects.filter(is_issued=False)
    return render(request ,"admin/issueRequests.html", {"requests":issuerequests,'user':request.user})

@user_passes_test(lambda user:user.is_admin)
def issueBookToStudent(request,student_id, book_id):
    book_object = Book.objects.get(id=book_id)
    student = Account.objects.get(id=student_id)
    issurequest = IssueRequest.objects.get(student=student, book=book_object)

    try:
        issueAccept = IssuedBooks.objects.create(issuerequest=issurequest,issuedby=student)
        issueAccept.save()
        issurequest.is_issued = True
        issurequest.save()
        book_object.quantity -1 
        book_object.save()
        messages.success(request, "Book issued to student succesfully!")
    except KeyError as e:
        messages.error(request, "Failed to issue book!")

    return redirect("issueRequests")

@user_passes_test(lambda user:not user.is_admin)
def myBooks(request):
    student = request.user
    mybooks = IssuedBooks.objects.filter(issuedby=student)
    for b in mybooks:
        print(b.issuerequest.book.name)
    return render(request, "student/mybooks.html",{'mybooks':mybooks})