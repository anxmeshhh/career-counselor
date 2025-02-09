from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return redirect('login')  # If already signed up, go to login

        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login')  # After signing up, go to login page

    return render(request, "signup.html")  # Show signup page

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to main page
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")  # Show login page

def index(request):
    return render(request, "index.html")  # Loads main page after login
