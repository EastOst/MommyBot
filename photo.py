import os
import time

# 사진을 찍을 파일 경로 설정
photo_path = "/home/comstouch/photo.jpg"

# libcamera 명령어로 사진 찍기
def take_picture():
    try:
        # libcamera-still 명령어로 사진 촬영
        os.system(f"libcamera-still -o {photo_path}")
        print(f"사진 촬영 완료! 파일 경로: {photo_path}")
    except Exception as e:
        print(f"오류 발생: {e}")

# 사진 촬영 테스트
take_picture()

# 촬영한 사진을 3초 뒤에 자동으로 삭제
time.sleep(3)
os.remove(photo_path)
print("사진 파일이 삭제되었습니다.")

