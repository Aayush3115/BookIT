from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class User(models.Model):
#     first_name=models.CharField(max_length=20)
#     last_name=models.CharField(max_length=20)
#     email=models.EmailField()

class Movie(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    duration=models.DurationField
    genre=models.CharField(max_length=20)
    release_date=models.DateField
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




