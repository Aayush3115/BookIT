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
    # poster_url=models.ImageField('')

class Theater(models.Model):
    threater_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=20)




