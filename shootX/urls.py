from django.urls import path
from django.contrib.auth import views as auth_views
from shootX import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'app'  # Nom du namespace


urlpatterns = [
    path('', views.client_access, name='home'),  # Page d'accueil par défaut
    path('', views.client_access, name='client_access'),
    path('gallery/<int:gallery_id>/', views.transfer_gallery, name='transfer_gallery'),
    path('download/<int:gallery_id>/',views.download_transfer_photos, name='download_transfer_photos'),  # ✅ Ajout de la route
    path('codes/', views.code_list, name='code_list'),
    path('codes/create/', views.create_code, name='create_code'),
    path('codes/update/<int:code_id>/', views.update_code, name='update_code'),
    path('codes/delete/<int:code_id>/', views.delete_code, name='delete_code'),
    path('codes/active/<int:code_id>/', views.active_code, name='active_code'),
    path('gallery/<int:gallery_id>/add_photos/', views.add_photos_to_gallery, name='add_photos_to_gallery'),

]

