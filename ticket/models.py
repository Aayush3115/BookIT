from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

# Create your models here.

# class User(models.Model):
#     first_name=models.CharField(max_length=20)
#     last_name=models.CharField(max_length=20)
#     email=models.EmailField()

class Movie(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    duration=models.DurationField(default=timedelta())
    genre=models.CharField(max_length=20)
    release_date=models.DateField(default='2000-01-01')
    rating=models.CharField(max_length=20)
    language=models.CharField(max_length=20)
    # showtime=models.TimeField(null=True)
    # poster_url=models.ImageField('')

    def __str__(self):
        return self.title

class Showtime(models.Model):
    movie=models.ForeignKey(Movie, on_delete=models.CASCADE,related_name='showtimes')
    time=models.TimeField(null=True)

    def __str__(self):
        return str(self.movie)

class Theater(models.Model):
    threater_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=20)

class Seat(models.Model):
    seat_id=models.AutoField(primary_key=True)
    seat_number=models.CharField(max_length=5)
    # is_available=models.BooleanField(default=True)

class Booking(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    showtime=models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seats=models.ManyToManyField(Seat)
    booking_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username}"




