from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home' ),
    path('signup/',views.signup_user, name= 'signup'),
    path('login/',views.login_user, name= 'login_user'),
    path('logout/', views.logout_user, name = 'logout'),
    path('events/', views.events, name = 'events'),
    path('ranking/', views.ranking, name = 'ranking')
]