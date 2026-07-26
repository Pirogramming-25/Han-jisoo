import os

# 반드시 paddleocr를 import하기 전에 설정해야 합니다.
# 한글이 포함된 사용자 경로에서 모델 파일을 읽지 못하는 문제를 방지합니다.
os.environ["PADDLE_PDX_CACHE_HOME"] = r"C:\paddlex_models"
os.environ["PADDLE_PDX_MODEL_SOURCE"] = "bos"

import re
from functools import lru_cache
from typing import Any

import cv2
import numpy as np
from paddleocr import PaddleOCR

from nutrient.rules import NUTRIENT_RULES, OCR_REPLACEMENTS


@lru_cache(maxsize=1)
def get_ocr_model() -> PaddleOCR:
    """
    PaddleOCR 모델을 최초 한 번만 생성하고 재사용합니다.
    """

    return PaddleOCR(
        lang="korean",
        ocr_version="PP-OCRv3",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        device="cpu",
    )


def read_image(image_path: str) -> np.ndarray:
    """
    한글이 포함된 Windows 경로에서도 이미지를 읽습니다.
    """

    image_bytes = np.fromfile(
        image_path,
        dtype=np.uint8,
    )

    image = cv2.imdecode(
        image_bytes,
        cv2.IMREAD_COLOR,
    )

    if image is None:
        raise ValueError(
            f"이미지 파일을 읽을 수 없습니다. 경로: {image_path}"
        )

    return image


def preprocess_image(image_path: str) -> np.ndarray:
    """
    영양성분표의 작은 글자를 OCR이 읽기 쉽도록 전처리합니다.
    """

    image = read_image(image_path)

    # 작은 글자 인식을 위해 2배 확대
    image = cv2.resize(
        image,
        None,
        fx=2.0,
        fy=2.0,
        interpolation=cv2.INTER_CUBIC,
    )

    # 흑백 변환
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY,
    )

    # 노이즈 감소
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0,
    )

    # 명암 대비 향상
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8),
    )

    enhanced = clahe.apply(gray)

    # 글자를 선명하게 만들기 위한 적응형 이진화
    binary = cv2.adaptiveThreshold(
        enhanced,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )

    # PaddleOCR는 높이, 너비, 채널의 3차원 이미지를 요구합니다.
    binary_bgr = cv2.cvtColor(
        binary,
        cv2.COLOR_GRAY2BGR,
    )

    return binary_bgr


def ensure_three_channels(image: np.ndarray) -> np.ndarray:
    """
    PaddleOCR에 전달할 이미지를 BGR 3채널로 맞춥니다.
    """

    if image is None:
        raise ValueError("OCR에 전달된 이미지가 비어 있습니다.")

    # 흑백 이미지: (height, width)
    if image.ndim == 2:
        image = cv2.cvtColor(
            image,
            cv2.COLOR_GRAY2BGR,
        )

    # 1채널 이미지: (height, width, 1)
    elif image.ndim == 3 and image.shape[2] == 1:
        image = cv2.cvtColor(
            image,
            cv2.COLOR_GRAY2BGR,
        )

    # 알파 채널 이미지: (height, width, 4)
    elif image.ndim == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGRA2BGR,
        )

    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError(
            f"OCR 이미지 형식이 올바르지 않습니다: {image.shape}"
        )

    return image


def _result_to_dict(result: Any) -> dict:
    """
    PaddleOCR 버전에 따라 결과 객체의 형태가 다를 수 있어
    안전하게 dict로 변환합니다.
    """

    if isinstance(result, dict):
        if isinstance(result.get("res"), dict):
            return result["res"]

        return result

    if hasattr(result, "json"):
        json_value = result.json

        if callable(json_value):
            json_value = json_value()

        if isinstance(json_value, dict):
            if isinstance(json_value.get("res"), dict):
                return json_value["res"]

            return json_value

    if hasattr(result, "res"):
        result_value = result.res

        if isinstance(result_value, dict):
            return result_value

    return {}


def collect_ocr_text(image: np.ndarray) -> str:
    """
    이미지에서 인식된 모든 문자열을 하나의 텍스트로 합칩니다.
    """

    image = ensure_three_channels(image)

    print("OCR 직전 이미지 shape:", image.shape)

    ocr = get_ocr_model()
    results = ocr.predict(image)

    texts: list[str] = []

    for result in results:
        result_data = _result_to_dict(result)

        recognized_texts = result_data.get(
            "rec_texts",
            [],
        )

        if not isinstance(recognized_texts, list):
            continue

        for recognized_text in recognized_texts:
            recognized_text = str(
                recognized_text
            ).strip()

            if recognized_text:
                texts.append(recognized_text)

    return "\n".join(texts)


def normalize_ocr_text(text: str) -> str:
    """
    OCR 결과의 영문 대소문자, 기호 및 자주 발생하는 오인식을 정리합니다.
    """

    text = text.lower()

    for old, new in OCR_REPLACEMENTS.items():
        text = text.replace(old, new)

    # 탭과 연속 공백을 한 칸으로 정리
    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    return text


def extract_calories(text: str) -> float | None:
    """
    OCR 문자열에서 열량 값을 추출합니다.
    """

    patterns = [
        r"(\d+(?:\.\d+)?)\s*kcal",
        r"(?:열량|칼로리)\s*[:：]?\s*(\d+(?:\.\d+)?)",
        r"(\d+(?:\.\d+)?)\s*킬로칼로리",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return float(match.group(1))

    return None


def extract_normal_nutrient_amount(
    text: str,
    keyword_pattern: str,
) -> float | None:
    """
    정상적으로 g 또는 mg가 인식된 영양성분 값을 추출합니다.

    예:
    탄수화물 29g
    지방 1.6g
    단백질 1g
    """

    patterns = [
        (
            rf"(?:{keyword_pattern})"
            rf"\s*[:：]?\s*"
            rf"(\d+(?:\.\d+)?)"
            rf"\s*(mg|g)"
        ),
        (
            rf"(?:{keyword_pattern})"
            rf".{{0,20}}?"
            rf"(\d+(?:\.\d+)?)"
            rf"\s*(mg|g)"
        ),
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if not match:
            continue

        amount = float(match.group(1))
        unit = match.group(2).lower()

        if unit == "mg":
            amount /= 1000

        return round(amount, 3)

    return None


def extract_ocr_misread_amount(
    text: str,
    keyword_pattern: str,
    nutrient_name: str,
) -> float | None:
    """
    OCR가 g를 숫자 9로 잘못 읽은 경우를 처리합니다.

    실제 문자열과 OCR 결과 예시:

    탄수화물 29g 9% → 탄수화물2999%
    지방 1.6g 3%    → 지방1693%
    단백질 1g 2%    → 단백질192%
    """

    pattern = (
        rf"(?:{keyword_pattern})"
        rf"\s*"
        rf"(\d{{1,3}})"
        rf"[g9]"
        rf"(\d{{1,2}})%"
    )

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    raw_amount = match.group(1)
    percent_text = match.group(2)

    amount = recover_decimal_amount(
        raw_amount=raw_amount,
        nutrient_name=nutrient_name,
        percent_text=percent_text,
    )

    return round(amount, 3)


def extract_nutrient_amount(
    text: str,
    keywords: list[str],
    nutrient_name: str,
) -> float | None:
    """
    특정 영양성분의 양을 추출합니다.

    먼저 정상적인 g/mg 형식을 찾고,
    찾지 못하면 OCR가 g를 9로 읽은 형식을 확인합니다.
    """

    if nutrient_name == "fat":
        # 트랜스지방과 포화지방은 제외하고
        # 총지방 또는 단독으로 적힌 지방만 검색
        keyword_pattern = (
            r"총지방|"
            r"(?<!트랜스)(?<!포화)지방|"
            r"total\s*fat"
        )
    else:
        keyword_pattern = "|".join(
            re.escape(keyword)
            for keyword in keywords
        )

    normal_amount = extract_normal_nutrient_amount(
        text,
        keyword_pattern,
    )

    if normal_amount is not None:
        return normal_amount

    return extract_ocr_misread_amount(
        text,
        keyword_pattern,
        nutrient_name,
    )


def extract_nutrition_from_image(
    image_path: str,
) -> dict:
    """
    영양성분표 이미지에서 칼로리, 탄수화물,
    단백질, 지방 값을 추출합니다.
    """

    original_image = read_image(image_path)
    processed_image = preprocess_image(image_path)

    # 전처리 이미지와 원본 이미지를 모두 분석합니다.
    # 특정 전처리에서 사라진 글자를 원본 OCR 결과로 보완합니다.
    processed_text = collect_ocr_text(
        processed_image
    )

    original_text = collect_ocr_text(
        original_image
    )

    ocr_text = (
        f"{processed_text}\n{original_text}"
    ).strip()

    normalized_text = normalize_ocr_text(
        ocr_text
    )

    result = {
        "calories": extract_calories(
            normalized_text
        ),
        "carbohydrate": extract_nutrient_amount(
            normalized_text,
            keywords=NUTRIENT_RULES[
                "carbohydrate"
            ]["keywords"],
            nutrient_name="carbohydrate",
        ),
        "protein": extract_nutrient_amount(
            normalized_text,
            keywords=NUTRIENT_RULES[
                "protein"
            ]["keywords"],
            nutrient_name="protein",
        ),
        "fat": extract_nutrient_amount(
            normalized_text,
            keywords=NUTRIENT_RULES[
                "fat"
            ]["keywords"],
            nutrient_name="fat",
        ),
        "ocr_text": ocr_text,
    }

    print("\n========== OCR 원문 ==========")
    print(ocr_text)

    print("========== 정규화 결과 ==========")
    print(normalized_text)

    print("========== 추출 결과 ==========")
    print(result)

    print("================================\n")

    return result

def recover_decimal_amount(
    raw_amount: str,
    nutrient_name: str,
    percent_text: str | None = None,
) -> float:
    """
    OCR가 소수점을 누락한 경우 값을 보정합니다.

    예:
    16 → 1.6
    25 → 2.5

    단, 모든 두 자리 숫자를 소수로 바꾸지는 않고
    영양성분 기준치 비율과 비교해 판단합니다.
    """

    normal_value = float(raw_amount)

    if len(raw_amount) < 2:
        return normal_value

    decimal_value = float(
        f"{raw_amount[:-1]}.{raw_amount[-1]}"
    )

    if not percent_text:
        return normal_value

    percent = float(percent_text)

    # 국내 영양성분 기준치의 대략적인 값
    daily_values = {
        "carbohydrate": 324,
        "protein": 55,
        "fat": 54,
    }

    daily_value = daily_values.get(nutrient_name)

    if not daily_value:
        return normal_value

    normal_percent = (
        normal_value / daily_value
    ) * 100

    decimal_percent = (
        decimal_value / daily_value
    ) * 100

    normal_difference = abs(
        normal_percent - percent
    )

    decimal_difference = abs(
        decimal_percent - percent
    )

    # 표에 적힌 퍼센트와 더 가까운 값을 선택
    if decimal_difference < normal_difference:
        return decimal_value

    return normal_value