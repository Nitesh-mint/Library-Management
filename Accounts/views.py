from django.shortcuts import render, HttpResponse

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth, messages

from .forms import RegisterForm
from .models import Account


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            level = form.cleaned_data['level']
            roll_number = form.cleaned_data['roll_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            if len(password) >=8:
                user = Account.objects.create_user(first_name=first_name,username=username, email=email, password=password, level=level, roll_number=roll_number)
                user.save()
                messages.success(request, "Account created succesfully")
                return redirect('login')
            else:
                messages.error(request, "Password must be 8 digist or more!")
        else:
            messages.error(request, "Failed to created account")
            return redirect('register')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':form})

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            if request.user.is_admin:
                messages.error(request, "Admin cannot login as Student!")
                auth.logout(request)
                return redirect('login')
            else:
                return redirect('student_home')
        else:
            messages.error(request, "Logged in Failed")
    return render(request, 'accounts/login.html')


def admin_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            if request.user.is_admin:
                return redirect('admin_home')
            else:
                messages.error(request, "Student cannot login as Admin!")
                auth.logout(request)
                return redirect('admin_login')
        else:
            messages.error(request, "Logged in Failed")
    return render(request, 'accounts/admin_login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('index')

user_passes_test(lambda user: user.is_admin)
def delete_student(request, id):
    student = Account.objects.get(id=id)
    student.delete()
    return HttpResponse("Student deleted successfully!")