import os
import tempfile

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import NutritionForm
from .models import Nutrition
from .services.ocr import extract_nutrition_from_image


def nutrition_list(request):
    nutritions = Nutrition.objects.all().order_by("-created_at")

    return render(
        request,
        "nutrient/nutrition_list.html",
        {
            "nutritions": nutritions,
        },
    )


def nutrition_create(request):
    if request.method == "POST":
        form = NutritionForm(request.POST, request.FILES)

        if form.is_valid():
            nutrition = form.save()

            return redirect(
                "nutrient:detail",
                pk=nutrition.pk,
            )
    else:
        form = NutritionForm()

    return render(
        request,
        "nutrient/nutrition_create.html",
        {
            "form": form,
        },
    )


def nutrition_detail(request, pk):
    nutrition = get_object_or_404(Nutrition, pk=pk)

    return render(
        request,
        "nutrient/nutrition_detail.html",
        {
            "nutrition": nutrition,
        },
    )


def nutrition_update(request, pk):
    nutrition = get_object_or_404(Nutrition, pk=pk)

    if request.method == "POST":
        form = NutritionForm(
            request.POST,
            request.FILES,
            instance=nutrition,
        )

        if form.is_valid():
            nutrition = form.save()

            return redirect(
                "nutrient:detail",
                pk=nutrition.pk,
            )
    else:
        form = NutritionForm(instance=nutrition)

    return render(
        request,
        "nutrient/nutrition_update.html",
        {
            "form": form,
            "nutrition": nutrition,
        },
    )


@require_POST
def nutrition_delete(request, pk):
    nutrition = get_object_or_404(Nutrition, pk=pk)
    nutrition.delete()

    return redirect("nutrient:list")


@require_POST
def analyze_nutrition(request):
    uploaded_image = request.FILES.get("image")

    if uploaded_image is None:
        return JsonResponse(
            {
                "success": False,
                "message": "분석할 이미지를 선택해주세요.",
            },
            status=400,
        )

    if not uploaded_image.content_type.startswith("image/"):
        return JsonResponse(
            {
                "success": False,
                "message": "이미지 파일만 업로드할 수 있습니다.",
            },
            status=400,
        )

    temporary_path = None

    try:
        suffix = os.path.splitext(uploaded_image.name)[1] or ".jpg"

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temporary_file:
            for chunk in uploaded_image.chunks():
                temporary_file.write(chunk)

            temporary_path = temporary_file.name

        result = extract_nutrition_from_image(temporary_path)

        return JsonResponse(
            {
                "success": True,
                "calories": result.get("calories"),
                "carbohydrate": result.get("carbohydrate"),
                "protein": result.get("protein"),
                "fat": result.get("fat"),
            }
        )

    except Exception as error:
        import traceback

        traceback.print_exc()

        return JsonResponse(
            {
                "success": False,
                "message": (
                    f"OCR 분석 오류: "
                    f"{type(error).__name__}: {error}"
                ),
            },
            status=500,
        )

    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)