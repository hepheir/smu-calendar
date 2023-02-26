# 빌드 방법 (개발)

Linux, Ubuntu, Mac의 개발환경이 권장됩니다.

Windows에서는 프로그램이 정상적으로 동작하지 않을 수도 있습니다.

## 의존성

본 프로젝트는 [Poetry](https://python-poetry.org)를 이용하여 의존성을 관리하고 있습니다.

다음의 명령을 통해 개발환경을 구축할 수 있습니다.

```shell
pip install poetry

poetry install
poetry run python src/main.py
```

## 이진파일 빌드

GitHub Action을 통해 주기적으로 캘린더를 갱신하고 있습니다.
자동화 작업 위해 이진파일을 빌드하여 사용하고 있습니다.
이진파일을 빌드하는 방법은 다음과 같습니다.

```shell
poetry run pyinstaller src/main.py -F -y --distpath bin
```
