from django.contrib import admin
from .models import Theater , User , Movie 
# Register your models here.
 
admin.site.register(User)
admin.site.register(Theater)
admin.site.register(Movie)
