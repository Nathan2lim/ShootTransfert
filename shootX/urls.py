from django.urls import path
from django.contrib.auth import views as auth_views
from shootX import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'app'  # Nom du namespace


urlpatterns = [
    path('home/',views.home, name = 'home'),
]

