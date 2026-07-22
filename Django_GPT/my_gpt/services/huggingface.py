from functools import lru_cache

from transformers import pipeline

from .common import get_pipeline_device


SENTIMENT_MODEL_ID = (
    "cardiffnlp/twitter-roberta-base-sentiment-latest"
)

SUMMARIZER_MODEL_ID = "sshleifer/distilbart-cnn-6-6"

MODERATOR_MODEL_ID = "unitary/toxic-bert"


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    return pipeline(
        task="text-classification",
        model=SENTIMENT_MODEL_ID,
        device=get_pipeline_device(),
    )


@lru_cache(maxsize=1)
def get_summarizer_pipeline():
    return pipeline(
        task="summarization",
        model=SUMMARIZER_MODEL_ID,
        device=get_pipeline_device(),
    )


@lru_cache(maxsize=1)
def get_moderator_pipeline():
    return pipeline(
        task="text-classification",
        model=MODERATOR_MODEL_ID,
        top_k=None,
        device=get_pipeline_device(),
    )


def run_sentiment(text):
    classifier = get_sentiment_pipeline()

    results = classifier(
        text,
        top_k=None,
        truncation=True,
    )

    if results and isinstance(results[0], list):
        results = results[0]

    normalized_results = [
        {
            "label": item["label"].lower(),
            "score": float(item["score"]),
        }
        for item in results
    ]

    normalized_results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return {
        "label": normalized_results[0]["label"],
        "score": normalized_results[0]["score"],
        "all_scores": normalized_results,
    }


def run_summarizer(text, regenerate=False):
    summarizer = get_summarizer_pipeline()

    options = {
        "max_length": 180,
        "min_length": 40,
        "truncation": True,
    }

    if regenerate:
        options.update(
            {
                "do_sample": True,
                "top_p": 0.9,
                "temperature": 0.8,
            }
        )
    else:
        options["do_sample"] = False

    result = summarizer(text, **options)
    summary = result[0]["summary_text"].strip()

    original_length = len(text)
    summary_length = len(summary)
    summary_ratio = (
        summary_length / original_length * 100
        if original_length
        else 0
    )

    return {
        "summary": summary,
        "original_length": original_length,
        "summary_length": summary_length,
        "summary_ratio": round(summary_ratio, 2),
    }


def run_moderation(text):
    moderator = get_moderator_pipeline()

    results = moderator(
        text,
        truncation=True,
    )

    if results and isinstance(results[0], list):
        results = results[0]

    normalized_results = [
        {
            "label": item["label"].lower(),
            "score": float(item["score"]),
        }
        for item in results
    ]

    normalized_results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    highest = normalized_results[0]

    return {
        "highest_label": highest["label"],
        "highest_score": highest["score"],
        "all_scores": normalized_results,
    }


def run_combo(text, regenerate=False):
    summary_result = run_summarizer(
        text,
        regenerate=regenerate,
    )

    summary = summary_result["summary"]

    sentiment_result = run_sentiment(summary)
    moderation_result = run_moderation(summary)

    if sentiment_result["label"] == "negative":
        sentiment_description = "부정적인 평가를 포함합니다."
    else:
        sentiment_description = (
            "강한 부정적 평가는 확인되지 않았습니다."
        )

    if moderation_result["highest_score"] >= 0.5:
        toxicity_description = (
            "유해 표현 가능성이 높습니다."
        )
    else:
        toxicity_description = (
            "심각한 유해 표현 가능성은 낮습니다."
        )

    overall_result = (
        f"{sentiment_description} "
        f"{toxicity_description}"
    )

    return {
        "summary": summary,
        "sentiment": sentiment_result,
        "toxicity": moderation_result,
        "overall_result": overall_result,
    }