from django.contrib import admin

from .models import InferenceHistory


@admin.register(InferenceHistory)
class InferenceHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "task",
        "created_at",
    )

    list_filter = (
        "task",
        "created_at",
    )

    search_fields = (
        "user__username",
        "input_text",
        "output_text",
    )

    readonly_fields = (
        "created_at",
    )