from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('users/search/', views.user_search, name='user_search'),
    path('profile/', views.my_profile, name='my_profile'),
    path('users/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    path('users/<str:username>/', views.user_feed, name='user_feed'),
    #path("stories/<int:user_id>/", views.story_detail, name="story_detail"),
    path('posts/search/', views.post_search, name='post_search'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/update/', views.update_post, name='update_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('posts/<int:post_id>/comments/', views.get_comments, name='get_comments'),
    path('posts/<int:post_id>/comments/create/', views.create_comment, name='create_comment'),
    path('comments/<int:comment_id>/update/', views.update_comment, name='update_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('stories/create/', views.create_story, name='create_story'),
    path('stories/<str:username>/', views.get_user_stories, name='get_user_stories'),
]