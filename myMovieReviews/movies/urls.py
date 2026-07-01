from django.urls import path
from . import views
from .api_views import ReviewListAPI, ReviewDetailAPI

urlpatterns = [
    path('', views.review_list, name='home'),
    
    path('movies/', views.review_list, name='review-list'),
    path('movies/create/', views.review_create, name='review-create'),
    path('movies/<int:pk>/', views.review_detail, name='review-detail'),
    path('movies/<int:pk>/update/', views.review_update, name='review-update'),
    path('movies/<int:pk>/delete/', views.review_delete, name='review-delete'),

    path('api/movies/', ReviewListAPI.as_view(), name='api-review-list'),
    path('api/movies/<int:pk>/', ReviewDetailAPI.as_view(), name='api-review-detail'),

    path('movies/ver2/', views.review_ver2, name='review-ver2'),
]
