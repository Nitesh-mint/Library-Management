from django.shortcuts import render

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
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
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            if len(password) >=8:
                user = Account.objects.create_user(first_name=first_name,username=username, email=email, password=password)
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
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Logged in Failed")
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')