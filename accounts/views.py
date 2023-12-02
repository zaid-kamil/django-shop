from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 
        # validate input
        if username == '' or password == '':
            messages.error(request, 'Please fill out all fields')
            return redirect('login')
        # authenticate user
        user = authenticate(request, username=username, password=password)
        # login user
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')
    
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('index')

def signup_view(request):
    if request.method == 'POST':
        # get form values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['confirm_password']
        # validate input
        if username == '' or email == '' or password == '' or password2 == '':
            messages.error(request, 'Please fill out all fields')
            return redirect('signup')
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        # create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'You have successfully registered')
        return redirect('login')
    else:
        return render(request, 'accounts/signup.html')
    
