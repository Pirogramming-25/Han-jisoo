# ideas/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 아이디어
    path('', views.idea_list, name='home'),
    path('ideas/', views.idea_list, name='idea-list'),
    path('ideas/create/', views.idea_create, name='idea-create'),
    path('ideas/manage/', views.idea_list, name='idea-manage'),
    path('ideas/<int:pk>/', views.idea_detail, name='idea-detail'),
    path('ideas/<int:pk>/update/', views.idea_update, name='idea-update'),
    path('ideas/<int:pk>/delete/', views.idea_delete, name='idea-delete'),
    path('ideas/<int:pk>/star/', views.idea_star, name='idea-star'),

    path('ideas/<int:pk>/interest/', views.idea_interest_ajax, name='idea-interest'),
    # 개발툴
    path('devtools/', views.devtool_manage, name='devtool-manage'),
    path('devtools/create/', views.devtool_create, name='devtool-add'),
    path('devtools/<int:pk>/', views.devtool_detail, name='devtool-detail'),
    path('devtools/<int:pk>/update/', views.devtool_update, name='devtool-update'),
    path('devtools/<int:pk>/delete/', views.devtool_delete, name='devtool-delete'),
]