import cv2
import time
from picamera2 import Picamera2
from adafruit_servokit import ServoKit

# 서보 모터 설정
SERVO_CHANNEL = 0  # 서보 모터가 연결된 PCA9685의 채널 번호
kit = ServoKit(channels=16)  # PCA9685에 16채널 서보 지원
move_servo_angle = 90  # 초기 각도 설정
kit.servo[SERVO_CHANNEL].angle = move_servo_angle

# 얼굴 검출을 위한 OpenCV Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Picamera2 설정
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})  # 설정 생성
picam2.configure(camera_config)  # 설정 적용

def move_servo(angle):
    """서보 모터를 주어진 각도로 이동"""
    global move_servo_angle
    move_servo_angle = max(0, min(180, angle))  # 각도를 0~180도로 제한
    kit.servo[SERVO_CHANNEL].angle = move_servo_angle  # ServoKit을 사용해 각도 설정

def track_face():
    """얼굴을 추적하며 서보 모터를 제어 (GUI 없이)"""
    picam2.start()
    frame_center = 640 // 2  # 프레임 중앙 좌표

    try:
        while True:
            frame = picam2.capture_array()
            time.sleep(0.03)  # 약 30 FPS로 제한
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # 얼굴 추적 및 로그 출력
            for (x, y, w, h) in faces:
                center_x = x + w // 2
                if center_x < frame_center - 20:
                    angle = move_servo_angle - 5  # 얼굴을 따라가며 왼쪽으로 이동
                elif center_x > frame_center + 20:
                    angle = move_servo_angle + 5  # 얼굴을 따라가며 오른쪽으로 이동
                else:
                    angle = move_servo_angle  # 얼굴이 중앙에 있으면 정지

                move_servo(angle)

            # 얼굴 검출 로그 출력
            print(f"Detected {len(faces)} face(s)")

            # 얼굴이 검출된 경우 이미지를 저장
            if len(faces) > 0:
                cv2.imwrite("face_detected.jpg", frame)
    finally:
        picam2.stop()

if __name__ == "__main__":
    track_face()

