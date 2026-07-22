사용한 Hugging Face 모델의 Model ID와 라이선스
모델의 입력 언어와 출력 레이블
실행 방법과 환경변수 설정 방법

<사용 모델>
1. 감정 분석 모델
- Model ID: cardiffnlp/twitter-roberta-base-sentiment-latest
- 라이선스: CC BY 4.0
- 입력 언어: 영어
- 출력 레이블:
    - negative
    - neutral
    - positive

2. 문서 요약 모델
- Model ID: sshleifer/distilbart-cnn-6-6
- 라이선스: Apache 2.0
- 입력 언어: 영어
- 출력 형태: 영어 요약문

3. 유해 표현 분석 모델
- Model ID: unitary/toxic-bert
- 라이선스: Apache 2.0
- 입력 언어: 영어
- 출력 레이블:
    - toxic
    - severe_toxic
    - obscene
    - threat
    - insult
    - identity_hate


<실행 방법>
1. Repository Clone
2. 가상환경 생성
3. 가상환경 활성화
4. 패키지 설치
5. 환경변수 파일 생성
6. 데이터베이스 적용
7. 관리자 계정 생성
8. 서버 실행

<환경변수 설정 방법>
`.env.example`

```env
SECRET_KEY=your-django-secret-key

# 공개 모델 사용 시 선택사항
HF_TOKEN=optional-hugging-face-token
```

실제 `.env` 파일에는 실제 값을 작성합니다.

```env
SECRET_KEY="actual-django-secret-key"
HF_TOKEN=
```

주의사항:
- `.env` 파일은 Git에 포함하지 않습니다.
- 실제 Secret Key나 Hugging Face Token을 코드에 직접 작성하지 않습니다.
- `.env.example`에는 실제 비밀값을 작성하지 않습니다.