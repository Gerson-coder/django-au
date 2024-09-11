from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home' ),
    path('signup/',views.signup_user, name= 'signup'),
    path('login/',views.login_user, name= 'login_user'),
    path('logout/', views.logout_user, name = 'logout'),
    path('events/', views.events, name = 'events'),
    path('ranking/', views.ranking, name = 'ranking'),
    path('members_fam/', views.members_fam, name = 'members_fam'),
    path('members_eliminated/', views.members_eliminated, name = 'members_eliminated'),
    path('delete-member/', views.delete_member, name='delete_member'),
    path('autocomplete-nickname/', views.autocomplete_nickname, name='autocomplete_nickname'),
    path('restart/',views.restart_member, name='restart_member'),
]