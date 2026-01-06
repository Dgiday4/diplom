from django.urls import path

from .views import login, logout, registrathion, profile_card, search_users

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('registrathion', registrathion, name='registrathion'),
    path('profile_card', profile_card, name='profile_card'),
    path('search', search_users, name='search_users'),

    ]