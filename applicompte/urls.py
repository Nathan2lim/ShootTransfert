from django.urls import path
from django.contrib.auth import views as auth_views
from applicompte import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'applicompte'  # Nom du namespace


urlpatterns = [
    path('login/',views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgetpassword/', views.forgetpassword, name='forgetpassword'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('resend-activation-link/<int:user_id>/', views.resend_activation_link, name='resend_activation_link'),
    path('myprofile/',views.profile, name = 'profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-users/<int:user_id>/', views.manage_user_staff_status, name='manage_user_staff_status'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('add-photos-user/<str:username>/', views.add_photos, name='add_photos'),
    path('search-users/', views.search_users, name='search_users'),
    path('search-users-page/', views.search_users_page, name='search_users_page'),
]

