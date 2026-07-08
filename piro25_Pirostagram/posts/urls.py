from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('users/<str:username>/', views.user_feed, name='user_feed'),
    path('profile/', views.my_profile, name='my_profile'),

]