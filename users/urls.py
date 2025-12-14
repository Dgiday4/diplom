from django.urls import path

from .views import login, logout, registrathion

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('registrathion', registrathion, name='registrathion')

    ]