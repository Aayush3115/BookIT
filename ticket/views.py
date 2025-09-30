from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import requests
import os
from django.contrib.auth.decorators import login_required



def home(request):
    movies=Movie.objects.all()
    showtimes=Showtime.objects.all()
    return render(request, 'home.html',{'movies':movies,'showtimes':showtimes} )

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
        api_key = os.getenv("api_key")
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

def select_seats(request):
    showtime_id = request.GET.get("showtime_id")
    if showtime_id:
        request.session["showtime_id"] = int(showtime_id)

    booked_seats = Booking.objects.filter(showtime_id=showtime_id).values_list("seats__seat_number", flat=True)
    booked_seats = list(booked_seats)

    return render(request, "selectseats.html", {"booked_seats": booked_seats})

def confirm_page(request):
    selected_seats = request.session.get("selected_seats", [])
    total_price = request.session.get("total_price", 0)

    return render(request, "confirmpage.html", {
        "selected_seats": selected_seats,
        "total_price": total_price
    })

def seat_selection(request):
    if request.method == "POST":
        selected_seats = request.POST.get("seats")
        total_price = request.POST.get("total_price")
        showtime_id = request.session.get("showtime_id")

        if not selected_seats or not showtime_id:
            messages.error(request, "Please select a showtime and seats.")
            return redirect("selectseats")

        # Store seats in session for payment page
        request.session["selected_seats"] = selected_seats.split(",")
        request.session["total_price"] = total_price

        # Redirect to payment page
        return redirect("confirmpage")

    # if GET request, redirect to seat selection page
    return redirect("selectseats")



@login_required
def payment_page(request):
    selected_seats = request.session.get("selected_seats", [])
    showtime_id = request.session.get("showtime_id")

    if not showtime_id or not selected_seats:
        messages.error(request, "Cannot complete booking. Please select seats and showtime.")
        return redirect("selectseats")

    showtime = Showtime.objects.get(id=showtime_id)

    if request.method == "POST":
        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            showtime=showtime
        )

        

        for seat_num in selected_seats:
            seat, created = Seat.objects.get_or_create(seat_number=seat_num)
            booking.seats.add(seat)

        booking.save()
        print(">>> Seats in session:", selected_seats)

        # Assign seats
        # seats = Seat.objects.filter(seat_number__in=selected_seats)
        # booking.seats.set(seats)
        # booking.save()

        # # Mark seats unavailable
        # for seat in seats:
        #     seat.is_available = False
        #     seat.save()

        # Clear session
        request.session.pop("selected_seats", None)
        request.session.pop("total_price", None)
        request.session.pop("showtime_id", None)

        messages.success(request, "Booking confirmed!")
        return redirect("home")  # or payment success page

    return render(request, "payment.html", {"selected_seats": selected_seats})
