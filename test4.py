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

def move_servo_with_threshold(target_angle, threshold=5):
    """서보 모터를 이동하되, 일정 각도 차이 이하이면 이동하지 않음"""
    global move_servo_angle
    if abs(move_servo_angle - target_angle) > threshold:  # 임계값을 초과할 경우에만 이동
        move_servo_angle = max(0, min(180, target_angle))  # 각도 제한
        kit.servo[SERVO_CHANNEL].angle = move_servo_angle

def detect_faces_dnn(frame):
    """DNN을 사용해 가장 가까운 얼굴 검출"""
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    closest_face = None
    max_area = 0

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")
            width = x1 - x
            height = y1 - y
            area = width * height  # 얼굴 크기 계산

            if area > max_area:
                max_area = area
                closest_face = (x, y, width, height)

    return closest_face  # 가장 큰 얼굴만 반환

def track_face():
    """가장 가까운 얼굴을 추적하며 서보 모터를 제어"""
    last_known_position = None  # 마지막 얼굴 중심 위치
    picam2.start()
    frame_center = 320 // 2  # 화면 중앙 (x 좌표 기준)

    try:
        while True:
            frame = picam2.capture_array()
            closest_face = detect_faces_dnn(frame)

            if closest_face:
                x, y, w, h = closest_face
                center_x = x + w // 2

                if last_known_position is None:
                    last_known_position = center_x

                # 좌표 변화가 작을 경우 움직이지 않음
                if abs(center_x - last_known_position) > 10:  # 허용 범위 10 픽셀
                    if center_x < frame_center - 20:
                        target_angle = move_servo_angle - 10  # 왼쪽으로 이동
                    elif center_x > frame_center + 20:
                        target_angle = move_servo_angle + 10  # 오른쪽으로 이동
                    else:
                        target_angle = move_servo_angle

                    # 서보 모터 이동
                    move_servo_with_threshold(target_angle, threshold=5)
                    last_known_position = center_x
            else:
                print("No face detected. Staying in the last position.")

            # 디버그 정보 출력
            print(f"Closest face: {closest_face}")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Moving to center position...")
        move_servo_with_threshold(90)  # Ctrl+C 누르면 서보 모터가 중앙으로 복귀
    finally:
        picam2.stop()
        print("Resources released. Program terminated.")

if __name__ == "__main__":
    track_face()

