from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('users/search/', views.user_search, name='user_search'),
    path('profile/', views.my_profile, name='my_profile'),
    path('users/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    path('users/<str:username>/', views.user_feed, name='user_feed'),
    path('posts/search/', views.post_search, name='post_search'),
    path('posts/create/', views.post_create, name='post_create'),
]