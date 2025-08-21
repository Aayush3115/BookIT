from django.urls import path
from .views import * 
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/',register_page,name='register'),
    path('',home,name='home'),
    path('movie',movie_page,name='movie'),
    path('selectseats',select_seats,name='selectseats'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns+= staticfiles_urlpatterns()