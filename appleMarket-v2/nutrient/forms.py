from django import forms

from .models import Nutrition


class NutritionForm(forms.ModelForm):
    class Meta:
        model = Nutrition

        fields = [
            "title",
            "image",
            "calories",
            "carbohydrate",
            "protein",
            "fat",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "제목을 입력해주세요.",
                    "class": "form-input",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                    "class": "form-file-input",
                }
            ),
            "calories": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "placeholder": "OCR 분석 후 자동 입력됩니다.",
                    "class": "form-input",
                }
            ),
            "carbohydrate": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "placeholder": "OCR 분석 후 자동 입력됩니다.",
                    "class": "form-input",
                }
            ),
            "protein": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "placeholder": "OCR 분석 후 자동 입력됩니다.",
                    "class": "form-input",
                }
            ),
            "fat": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "placeholder": "OCR 분석 후 자동 입력됩니다.",
                    "class": "form-input",
                }
            ),
        }

        labels = {
            "title": "제목",
            "image": "영양성분표 이미지",
            "calories": "칼로리(kcal)",
            "carbohydrate": "탄수화물(g)",
            "protein": "단백질(g)",
            "fat": "지방(g)",
        }