from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/', views.login, name='login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('logout/', views.logout, name='logout'),
    path('delete/<int:id>', views.delete_student, name='delete_student'),
]
