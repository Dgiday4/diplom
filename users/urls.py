from django.urls import path

from .views import *

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('registrathion', registrathion, name='registrathion'),
    path('profile_card/', profile_card, name='profile_card'),
    path('search', search_users, name='search_users'),

    path('add_friend/<int:user_id>/', add_friend, name='add_friend'),
    path('remove_friend/<int:user_id>/', remove_friend, name='remove_friend'),
    path('friends/', friends_list, name='friends_list'),
    path('friends/<int:user_id>/', user_friends_list, name='user_friends_list'),

    ]