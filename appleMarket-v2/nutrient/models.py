from django.db import models


class Nutrition(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="nutrition/")
    
    calories = models.FloatField(
        verbose_name="칼로리(kcal)",
        null=True,
        blank=True,
    )
    carbohydrate = models.FloatField(
        verbose_name="탄수화물(g)",
        null=True,
        blank=True,
    )
    protein = models.FloatField(
        verbose_name="단백질(g)",
        null=True,
        blank=True,
    )
    fat = models.FloatField(
        verbose_name="지방(g)",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="작성일",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="수정일",
    )

    def __str__(self):
        return self.title