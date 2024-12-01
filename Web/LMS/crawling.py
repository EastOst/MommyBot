from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 사용자 로그인 정보
user_id = ""
password = ""

# ChromeDriver 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # 로그인 페이지로 이동
    driver.get('https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https%3A%2F%2Flms.ssu.ac.kr%2Fxn-sso%2Fgw-cb.php')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'userid'))).send_keys(user_id)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pwd'))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_login'))).click()
    print("로그인 성공")

    # 마이페이지로 이동
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="https://lms.ssu.ac.kr/mypage"]'))).click()
    print("마이페이지로 이동 성공")

    # iframe 전환 및 캘린더 데이터 확인
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe')))
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')

    # iframe 탐색
    for i, iframe in enumerate(iframes):
        driver.switch_to.frame(iframe)
        try:
            if driver.find_elements(By.CSS_SELECTOR, '.xndb-calendar-link'):
                print(f"캘린더 링크를 iframe {i}에서 발견")
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.xndb-calendar-link'))).click()
                break
        except Exception as e:
            print(f"iframe {i}에서 오류 발생: {e}")
        finally:
            driver.switch_to.default_content()

    # 기본 프레임으로 전환
    driver.switch_to.default_content()

    # 일정 탭 클릭
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "agenda"))).click()
    print("일정 탭 클릭 성공")

    # JavaScript 로드 완료 대기
    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    print("JavaScript 로드 완료")

    # 캘린더 데이터 로드 대기
    agenda_wrapper = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".agenda-wrapper.active"))
    )
    print("Success: The '.agenda-wrapper.active' element was found!")

    # 자식 요소가 로드될 때까지 대기
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".agenda-wrapper.active .agenda-day"))
    )
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".agenda-wrapper.active .agenda-event__container"))
    )

    # 날짜와 이벤트 정보를 저장할 딕셔너리
    events_by_date = {}

    # 날짜와 이벤트 매핑
    days = agenda_wrapper.find_elements(By.CSS_SELECTOR, ".agenda-day")
    events = agenda_wrapper.find_elements(By.CSS_SELECTOR, ".agenda-event__container")

    for i, day in enumerate(days):
        try:
            # 날짜 추출
            date_element = day.find_element(By.CLASS_NAME, "agenda-date")
            date_text = date_element.text.strip()

            # 이벤트 컨테이너 처리
            event_container = events[i]
            event_list = event_container.find_element(By.CLASS_NAME, "agenda-event__list")
            event_items = event_list.find_elements(By.CLASS_NAME, "agenda-event__item")

            # 이벤트 정보 저장
            event_details = []
            for event in event_items:
                # 이벤트 제목과 시간
                title = event.find_element(By.CLASS_NAME, "agenda-event__title").text.strip()
                time = event.find_element(By.CLASS_NAME, "agenda-event__time").text.strip()

                # 과목명 추출 (정확한 요소 탐색)
                try:
                    subject_elements = event.find_elements(By.CLASS_NAME, "screenreader-only")
                    subject = [s.text for s in subject_elements if "캘린더" in s.text][-1].strip()
                except IndexError:
                    subject = "과목 정보 없음"

                # 이벤트 정보 추가
                event_details.append({"title": title, "time": time, "subject": subject})

            # 날짜별 이벤트 저장
            events_by_date[date_text] = event_details

        except Exception as e:
            print(f"Error processing events for date {date_text}: {e}")

    # 출력
    for date, events in events_by_date.items():
        print(f"Date: {date}")
        for event in events:
            print(f"  - Title: {event['title']}, Time: {event['time']}, Subject: {event['subject']}")

    # 디버깅용 HTML 저장
    with open("page_source.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)
    print("Page source saved to 'page_source.html'.")

except Exception as e:
    print("Error occurred:", e)

finally:
    # 브라우저 종료
    time.sleep(5)
    driver.quit()
