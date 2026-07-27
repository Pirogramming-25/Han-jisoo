from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            "title",
            "content",
            "region",
            "user",
            "price",
            "photo",
            "nutrition_image",
            "calories",
            "carbohydrate",
            "protein",
            "fat",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "제목을 입력하세요",
                }
            ),
            "content": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "내용을 입력하세요",
                }
            ),
            "region": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "지역을 입력하세요",
                }
            ),
            "user": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),
            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "nutrition_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "calories": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": 0,
                    "placeholder": "OCR 분석 후 자동 입력",
                }
            ),
            "carbohydrate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": 0,
                    "placeholder": "OCR 분석 후 자동 입력",
                }
            ),
            "protein": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": 0,
                    "placeholder": "OCR 분석 후 자동 입력",
                }
            ),
            "fat": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": 0,
                    "placeholder": "OCR 분석 후 자동 입력",
                }
            ),
        }