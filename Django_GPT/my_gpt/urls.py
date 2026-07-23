from django.urls import path

from . import views


app_name = "my_gpt"

urlpatterns = [
    path(
        "sentiment/",
        views.sentiment_page,
        name="sentiment",
    ),
    path(
        "sentiment/run/",
        views.run_sentiment_view,
        name="run_sentiment",
    ),

    path(
        "summarize/",
        views.summarize_page,
        name="summarize",
    ),

    path(
        "summarize/run/",
        views.run_summarize_view,
        name="run_summarize",
    ),
    path(
        "moderate/",
        views.moderate_page,
        name="moderate",
    ),
    path(
        "moderate/run/",
        views.run_moderate_view,
        name="run_moderate",
    ),
    path(
        "combo/",
        views.combo_page,
        name="combo",
    ),
    path(
        "combo/run/",
        views.run_combo_view,
        name="run_combo",
    ),
]