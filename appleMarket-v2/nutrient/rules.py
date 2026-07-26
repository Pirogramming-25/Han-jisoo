NUTRIENT_RULES = {
    "carbohydrate": {
        "keywords": [
            "탄수화물",
            "탄수화믈",
            "탄수화물량",
            "carbohydrate",
        ],
    },
    "protein": {
        "keywords": [
            "단백질",
            "단백칠",
            "단백질량",
            "protein",
        ],
    },
    "fat": {
        "keywords": [
            "총지방",
            "지방",
            "지방량",
            "total fat",
            "fat",
        ],
    },
}


OCR_REPLACEMENTS = {
    "㎉": "kcal",
    "k cal": "kcal",
    "kca1": "kcal",
    "kca!": "kcal",
    "kca|": "kcal",
    "ｍｇ": "mg",
    "ｇ": "g",
    ",": ".",
}