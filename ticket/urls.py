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
    path('confirmpage',confirm_page,name='confirmpage'),
    path('seat_selection/', seat_selection, name='seat_selection'),
    path('payment/', payment_page, name='payment'),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns+= staticfiles_urlpatterns()