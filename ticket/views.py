from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import requests

def home(request):
    movies=Movie.objects.all()
    return render(request, 'home.html',{'movies':movies})

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        User.objects.create_user(
            username=username,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'register.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


def movie_page(request):
    movies = Movie.objects.all()
    query = request.GET.get('q')  
    search_results = None

    if query:
        api_key = "4909b29c"
        url = f"http://www.omdbapi.com/?s={query}&apikey={api_key}&type=movie"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            search_results = data.get("Search")  
        else:
            search_results = []

    return render(request, "movies.html", {
        "movies": movies,
        "search_results": search_results
    })

