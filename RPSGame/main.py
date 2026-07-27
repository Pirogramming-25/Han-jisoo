import math
import time
from pathlib import Path

import cv2 as cv
import mediapipe as mp
from mediapipe.tasks.python import vision

from visualization import draw_manual, print_RSP_result


# main.py의 상위 폴더에 있는 모델 파일 경로
MODEL_PATH = (
    Path(__file__).resolve().parent
    / "hand_landmarker.task"
)

# 비동기 콜백에서 전달받은 최신 인식 결과를 저장
latest_result = None


def calculate_distance(point1, point2):
    """
    두 랜드마크 사이의 2차원 거리를 계산합니다.

    point1, point2는 MediaPipe 랜드마크 객체이며
    각각 x, y 좌표를 가지고 있습니다.
    """
    return math.sqrt(
        (point1.x - point2.x) ** 2
        + (point1.y - point2.y) ** 2
    )


def is_finger_extended(hand_landmarks, pip_index, tip_index):
    """
    한 손가락이 펴졌는지 판단합니다.

    손끝 TIP과 손목 사이 거리,
    중간 마디 PIP와 손목 사이 거리를 비교합니다.
    """
    wrist = hand_landmarks[0]
    pip = hand_landmarks[pip_index]
    tip = hand_landmarks[tip_index]

    pip_distance = calculate_distance(wrist, pip)
    tip_distance = calculate_distance(wrist, tip)

    # 손끝이 중간 마디보다 손목에서 더 멀면 펴진 것으로 판단
    return tip_distance > pip_distance


def classify_rps(hand_landmarks):
    """
    엄지를 제외한 검지, 중지, 약지, 소지의 상태를 이용해
    가위, 바위, 보를 판별합니다.

    반환값:
    0 -> Rock
    1 -> Paper
    2 -> Scissors
    None -> 판별 불가
    """
    index_extended = is_finger_extended(
        hand_landmarks,
        pip_index=6,
        tip_index=8,
    )

    middle_extended = is_finger_extended(
        hand_landmarks,
        pip_index=10,
        tip_index=12,
    )

    ring_extended = is_finger_extended(
        hand_landmarks,
        pip_index=14,
        tip_index=16,
    )

    pinky_extended = is_finger_extended(
        hand_landmarks,
        pip_index=18,
        tip_index=20,
    )

    finger_states = [
        index_extended,
        middle_extended,
        ring_extended,
        pinky_extended,
    ]

    # 바위: 네 손가락이 모두 접힘
    if finger_states == [False, False, False, False]:
        return 0

    # 보: 네 손가락이 모두 펴짐
    if finger_states == [True, True, True, True]:
        return 1

    # 가위: 검지와 중지만 펴짐
    if finger_states == [True, True, False, False]:
        return 2

    # 그 외의 손 모양
    return None


def save_result(
    result,
    output_image,
    timestamp_ms,
):
    """
    MediaPipe가 손 인식을 마치면 자동으로 호출되는 콜백 함수입니다.
    최신 결과를 전역 변수에 저장합니다.
    """
    global latest_result
    latest_result = result


def run_rps_game():
    """
    웹캠 영상을 실시간으로 받아
    손 랜드마크와 가위바위보 결과를 출력합니다.
    """
    if not MODEL_PATH.exists():
        print("hand_landmarker.task 파일을 찾을 수 없습니다.")
        print(f"현재 확인한 경로: {MODEL_PATH}")
        return

    with open(MODEL_PATH, "rb") as model_file:
        model_data = model_file.read()

    base_options = mp.tasks.BaseOptions(
        model_asset_buffer=model_data
    )

    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.LIVE_STREAM,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        result_callback=save_result,
    )

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    start_time = time.monotonic()
    last_timestamp_ms = -1

    with vision.HandLandmarker.create_from_options(
        options
    ) as landmarker:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("카메라 프레임을 읽을 수 없습니다.")
                break

            # 거울처럼 보이도록 좌우 반전
            frame = cv.flip(frame, 1)

            # OpenCV는 BGR, MediaPipe는 RGB 사용
            rgb_frame = cv.cvtColor(
                frame,
                cv.COLOR_BGR2RGB,
            )

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_frame,
            )

            # 이전 프레임보다 계속 증가하는 timestamp
            timestamp_ms = int(
                (time.monotonic() - start_time) * 1000
            )

            # 이전 timestamp와 같거나 작으면 강제로 1 증가
            if timestamp_ms <= last_timestamp_ms:
                timestamp_ms = last_timestamp_ms + 1

            last_timestamp_ms = timestamp_ms

            landmarker.detect_async(
                mp_image,
                timestamp_ms,
            )

            rps_result = None

            if (
                latest_result is not None
                and latest_result.hand_landmarks
            ):
                hand_landmarks = (
                    latest_result.hand_landmarks[0]
                )

                rps_result = classify_rps(
                    hand_landmarks
                )

            # 손 랜드마크 그리기
            frame = draw_manual(
                frame,
                latest_result,
            )

            # Rock, Paper, Scissors 출력
            frame = print_RSP_result(
                frame,
                rps_result,
            )

            cv.imshow(
                "Rock Paper Scissors",
                frame,
            )

            # q 키를 누르면 종료
            if cv.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    run_rps_game()