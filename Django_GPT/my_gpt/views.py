import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .decorators import model_login_required
from .models import InferenceHistory
from .services.huggingface import (
    run_combo,
    run_moderation,
    run_sentiment,
    run_summarizer,
)

logger = logging.getLogger(__name__)

def sentiment_page(request):
    histories = []

    if request.user.is_authenticated:
        histories = (
            InferenceHistory.objects
            .filter(
                user=request.user,
                task=InferenceHistory.Task.SENTIMENT,
            )[:5]
        )

    return render(
        request,
        "my_gpt/sentiment.html",
        {
            "active_tab": "sentiment",
            "histories": histories,
        },
    )

@require_POST
def run_sentiment_view(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {
                "error": "잘못된 요청입니다.",
            },
            status=400,
        )

    text = data.get("text")

    if not isinstance(text, str):
        return JsonResponse(
            {
                "error": "분석할 문장을 입력해주세요.",
            },
            status=400,
        )

    text = text.strip()

    if not text:
        return JsonResponse(
            {
                "error": "분석할 문장을 입력해주세요.",
            },
            status=400,
        )

    if len(text) > 1000:
        return JsonResponse(
            {
                "error": "문장은 1,000자 이하로 입력해주세요.",
            },
            status=400,
        )

    try:
        result = run_sentiment(text)
    except Exception:
        logger.exception("Sentiment model inference failed.")

        return JsonResponse(
            {
                "error": (
                    "모델 실행에 실패했습니다. "
                    "잠시 후 다시 시도해주세요."
                ),
            },
            status=502,
        )

    if request.user.is_authenticated:
        history = InferenceHistory.objects.create(
            user=request.user,
            task=InferenceHistory.Task.SENTIMENT,
            input_text=text,
            output_text=(
                f"{result['label']} "
                f"{result['score'] * 100:.2f}%"
            ),
            result_data=result,
        )

        created_at = history.created_at.strftime(
            "%Y-%m-%d %H:%M",
        )
    else:
        created_at = ""

    return JsonResponse(
        {
            "input_text": text,
            "label": result["label"],
            "score": result["score"],
            "all_scores": result["all_scores"],
            "created_at": created_at,
        }
    )

@model_login_required
def summarize_page(request):
    histories = (
        InferenceHistory.objects
        .filter(
            user=request.user,
            task=InferenceHistory.Task.SUMMARIZE,
        )[:5]
    )

    return render(
        request,
        "my_gpt/summarize.html",
        {
            "active_tab": "summarize",
            "histories": histories,
        },
    )



@model_login_required
def moderate_page(request):
    histories = (
        InferenceHistory.objects
        .filter(
            user=request.user,
            task=InferenceHistory.Task.MODERATE,
        )[:5]
    )

    return render(
        request,
        "my_gpt/moderate.html",
        {
            "active_tab": "moderate",
            "histories": histories,
        },
    )


@model_login_required
def combo_page(request):
    histories = (
        InferenceHistory.objects
        .filter(
            user=request.user,
            task=InferenceHistory.Task.COMBO,
        )[:5]
    )

    return render(
        request,
        "my_gpt/combo.html",
        {
            "active_tab": "combo",
            "histories": histories,
        },
    )

@require_POST
@model_login_required
def run_summarize_view(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {
                "error": "잘못된 요청입니다.",
            },
            status=400,
        )

    text = data.get("text")

    if not isinstance(text, str):
        return JsonResponse(
            {
                "error": "요약할 문서를 입력해주세요.",
            },
            status=400,
        )

    text = text.strip()

    if not text:
        return JsonResponse(
            {
                "error": "요약할 문서를 입력해주세요.",
            },
            status=400,
        )

    if len(text) < 100:
        return JsonResponse(
            {
                "error": (
                    "요약할 문서는 "
                    "100자 이상 입력해주세요."
                ),
            },
            status=400,
        )

    if len(text) > 5000:
        return JsonResponse(
            {
                "error": (
                    "문서는 5,000자 이하로 "
                    "입력해주세요."
                ),
            },
            status=400,
        )

    try:
        result = run_summarizer(text)
    except Exception:
        logger.exception(
            "Summarization model inference failed."
        )

        return JsonResponse(
            {
                "error": (
                    "모델 실행에 실패했습니다. "
                    "잠시 후 다시 시도해주세요."
                ),
            },
            status=502,
        )

    history = InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.SUMMARIZE,
        input_text=text,
        output_text=result["summary"],
        result_data=result,
    )

    return JsonResponse(
        {
            "input_text": text,
            "summary": result["summary"],
            "original_length": result["original_length"],
            "summary_length": result["summary_length"],
            "summary_ratio": result["summary_ratio"],
            "created_at": history.created_at.strftime(
                "%Y-%m-%d %H:%M"
            ),
        }
    )

@require_POST
@model_login_required
def run_moderate_view(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {
                "error": "잘못된 요청입니다.",
            },
            status=400,
        )

    text = data.get("text")

    if not isinstance(text, str):
        return JsonResponse(
            {
                "error": "분석할 문장을 입력해주세요.",
            },
            status=400,
        )

    text = text.strip()

    if not text:
        return JsonResponse(
            {
                "error": "분석할 문장을 입력해주세요.",
            },
            status=400,
        )

    if len(text) > 1000:
        return JsonResponse(
            {
                "error": (
                    "문장은 1,000자 이하로 "
                    "입력해주세요."
                ),
            },
            status=400,
        )

    try:
        result = run_moderation(text)
    except Exception:
        logger.exception(
            "Moderation model inference failed."
        )

        return JsonResponse(
            {
                "error": (
                    "모델 실행에 실패했습니다. "
                    "잠시 후 다시 시도해주세요."
                ),
            },
            status=502,
        )

    history = InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.MODERATE,
        input_text=text,
        output_text=(
            f"{result['highest_label']} "
            f"{result['highest_score'] * 100:.2f}%"
        ),
        result_data=result,
    )

    return JsonResponse(
        {
            "input_text": text,
            "highest_label": result["highest_label"],
            "highest_score": result["highest_score"],
            "all_scores": result["all_scores"],
            "created_at": history.created_at.strftime(
                "%Y-%m-%d %H:%M"
            ),
        }
    )

@require_POST
@model_login_required
def run_combo_view(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {
                "error": "잘못된 요청입니다.",
            },
            status=400,
        )

    text = data.get("text")
    regenerate = data.get("regenerate", False)

    if not isinstance(text, str):
        return JsonResponse(
            {
                "error": "분석할 내용을 입력해주세요.",
            },
            status=400,
        )

    if not isinstance(regenerate, bool):
        return JsonResponse(
            {
                "error": "잘못된 요청입니다.",
            },
            status=400,
        )

    text = text.strip()

    if not text:
        return JsonResponse(
            {
                "error": "분석할 내용을 입력해주세요.",
            },
            status=400,
        )

    if len(text) < 200:
        return JsonResponse(
            {
                "error": (
                    "복합 분석 내용은 "
                    "200자 이상 입력해주세요."
                ),
            },
            status=400,
        )

    if len(text) > 5000:
        return JsonResponse(
            {
                "error": (
                    "복합 분석 내용은 "
                    "5,000자 이하로 입력해주세요."
                ),
            },
            status=400,
        )

    try:
        result = run_combo(
            text,
            regenerate=regenerate,
        )
    except Exception:
        logger.exception(
            "Combo model inference failed."
        )

        return JsonResponse(
            {
                "error": (
                    "모델 실행에 실패했습니다. "
                    "잠시 후 다시 시도해주세요."
                ),
            },
            status=502,
        )

    history = InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.COMBO,
        input_text=text,
        output_text=result["overall_result"],
        result_data=result,
    )

    return JsonResponse(
        {
            "input_text": text,
            "summary": result["summary"],
            "sentiment": result["sentiment"],
            "toxicity": result["toxicity"],
            "overall_result": result["overall_result"],
            "created_at": history.created_at.strftime(
                "%Y-%m-%d %H:%M"
            ),
        }
    )