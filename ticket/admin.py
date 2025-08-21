from django.contrib import admin
from .models import Theater , Showtime , Movie 
# Register your models here.
 
admin.site.register(Showtime)
admin.site.register(Theater)
admin.site.register(Movie)
