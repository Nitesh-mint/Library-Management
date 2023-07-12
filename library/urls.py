from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('student_home/', views.student_home, name='student_home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('add_book/', views.add_book, name='add_book'),
    path('books/', views.available_books, name='available_books'),
    path('students/', views.students, name='students'),
    path('issue/', views.issueBook, name='issuebook'),
    path('issue_noform/<int:book_id>/', views.issueBook_noform, name=''),
    path('issueRequestlist/',views.issueRequests, name="issueRequests" ),
    path('issueBookToStudent/<int:student_id>/<int:book_id>/',views.issueBookToStudent, name="issueBookToStudent"),
    path('mybooks/',views.myBooks, name="mybooks"),
]
