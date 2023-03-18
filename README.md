# 상명대학교 학사일정 (iCloud 캘린더)

상명대학교의 학사일정을 iCloud 캘린더에서 구독할 수 있는 형태로 가공한 것 입니다.

Mac을 사용하는 Apple 사용자에게 유용합니다.

## 사용 방법 (캘린더 구독 방법)

(Apple 홈페이지에서 확인하기: https://support.apple.com/ko-kr/HT202361)

1. Mac에서 Calendar 앱을 열고, '파일' > '새로운 캘린더 구독'을 선택합니다. (혹은 <kbd>⌥</kbd>+<kbd>⌘</kbd>+<kbd>S</kbd>)

2. 캘린더의 웹 주소로 다음의 URL을 입력합니다.
    ```
    https://hepheir.github.io/smu-calendar/calendar.ics
    ```
3. 나머지 정보를 자유롭게 입력한 후, '확인'을 선택합니다.

## 사용 모습

정상적으로 캘린더를 구독하였을 때의 모습입니다.

![image](https://user-images.githubusercontent.com/19310326/221437658-dd1dbfea-b2a7-4cfa-90f9-e066415c1ada.png)

---

# 개발

Python 3.10에서 개발되었으며, 외부 의존성으로 `requests`와 `ics` 패키지를 사용하고 있습니다.

개발환경을 구축하려면 다음의 명령어로 필요한 의존성을 설치 할 수 있습니다:

```shell
pip install -r requirements.txt
```

## 참고 문서

상명대학교 학사일정
: https://www.smu.ac.kr/ko/life/academicCalendar.do

iCalender(*.ics) 명세
: https://icalendar.org

Pip의 ics.py 패키지 명세
: https://icspy.readthedocs.io/en/stable/index.html