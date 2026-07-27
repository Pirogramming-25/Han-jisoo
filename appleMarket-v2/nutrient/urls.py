from django.urls import path
from . import views

app_name = "nutrient"

urlpatterns = [
    path("", views.nutrition_list, name="list"),
    path("create/", views.nutrition_create, name="create"),
    path("analyze/", views.analyze_nutrition, name="analyze"),
    path("detail/<int:pk>/", views.nutrition_detail, name="detail"),
    path("update/<int:pk>/update/", views.nutrition_update, name="update"),
    path("delete/<int:pk>/delete/", views.nutrition_delete, name="delete"),
]