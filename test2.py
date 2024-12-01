import cv2
import time
from picamera2 import Picamera2
from adafruit_servokit import ServoKit
import numpy as np

# 서보 모터 설정
SERVO_CHANNEL = 0
kit = ServoKit(channels=16)
move_servo_angle = 90
kit.servo[SERVO_CHANNEL].angle = move_servo_angle

# DNN 기반 얼굴 검출 모델 로드
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

# Picamera2 설정
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (320, 240), "format": "RGB888"})
picam2.configure(camera_config)

def smooth_servo_movement(target_angle, step=5):
    """서보 모터를 점진적으로 이동"""
    global move_servo_angle
    while move_servo_angle != target_angle:
        try:
            if move_servo_angle < target_angle:
                move_servo_angle += step
            elif move_servo_angle > target_angle:
                move_servo_angle -= step

            # 각도 제한 (0~180도)
            move_servo_angle = max(0, min(180, move_servo_angle))
            kit.servo[SERVO_CHANNEL].angle = move_servo_angle
            time.sleep(0.005)  # 속도 조정
        except OSError as e:
            print(f"I2C communication error: {e}. Retrying...")
            time.sleep(0.1)  # 잠시 대기 후 재시도

def calculate_smooth_center(new_center, prev_center=None, alpha=0.5):
    """가중 평균으로 중심 좌표를 부드럽게 계산"""
    if prev_center is None:
        return new_center
    return int(alpha * new_center + (1 - alpha) * prev_center)

def detect_faces_dnn(frame):
    """DNN을 사용해 얼굴 검출"""
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    faces = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")
            faces.append((x, y, x1 - x, y1 - y))
    return faces

def track_face():
    """얼굴을 추적하며 서보 모터를 제어"""
    last_known_position = None  # 마지막 얼굴 중심 위치
    picam2.start()
    frame_center = 320 // 2  # 화면 중앙 (x 좌표 기준)

    try:
        while True:
            # Picamera로 프레임 캡처
            frame = picam2.capture_array()
            faces = detect_faces_dnn(frame)

            if len(faces) > 0:
                # 얼굴이 하나라도 감지된 경우
                for (x, y, w, h) in faces:
                    center_x = x + w // 2  # 얼굴 중심 좌표
                    center_x = calculate_smooth_center(center_x, last_known_position)
                    last_known_position = center_x  # 마지막 얼굴 위치 업데이트

                    if center_x < frame_center - 20:
                        angle = move_servo_angle - 10  # 왼쪽으로 이동
                    elif center_x > frame_center + 20:
                        angle = move_servo_angle + 10  # 오른쪽으로 이동
                    else:
                        angle = move_servo_angle

                    # 각도 제한 확인
                    if angle < 0:
                        angle = 0
                    elif angle > 180:
                        angle = 180

                    # 서보 모터 이동
                    smooth_servo_movement(angle, step=10)
            else:
                # 얼굴이 감지되지 않은 경우, 마지막 위치를 유지
                print("No face detected. Staying in the last position.")

            # 디버그 정보 출력
            print(f"Detected {len(faces)} face(s): {faces}")
            time.sleep(0.05)  # 루프 속도

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Cleaning up...")
    finally:
        # Picamera와 서보 모터 정리
        picam2.stop()
        print("Resources released. Program terminated.")

if __name__ == "__main__":
    track_face()

